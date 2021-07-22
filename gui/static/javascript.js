
//selectElement is for keeping track of which Element's attribute should be changed, and draggedElement is
//for memoizing which element to drag.
let selectedElement = null, draggedElement = null;

//The directed graph will be send to the backend.
//need undirected graph to deal with keeping edges connected to elements that are being dragged around
let directedGraph = [], undirectedGraph = [];

let selectedSlot = {obj: null, elem: null, type: "input"};

var NS = "http://www.w3.org/2000/svg", elemWidth = 80, elemHeight = 40, slotWidth = 10, slotHeight = 10;

//the lists we are storing our Element and Edge objects in. Both objects have IDs which are stored in the JS object itself
//and HTML DOM element ID. The IDs correspond to the index at which they are stored in.
var elements = [], edges = [];

//the window we are drawing our elements in
let svgWindow = document.getElementById("canvas");

function getMousePosition(svgWindow, event) {
    var CTM = svgWindow.getScreenCTM();
    if (event.touches) { event = event.touches[0]; }
    return {
        x: (event.clientX - CTM.e) / CTM.a,
        y: (event.clientY - CTM.f) / CTM.d
    };
}

function bindSelectedElement(htmlElement){
    id = parseInt(htmlElement.id);
    selectedElement = elements[id];
    document.getElementById("elemAttribSelector1").value = selectedElement.kernelSize;
    document.getElementById("elemAttribSelector2").value = selectedElement.stride;
    document.getElementById("elemAttribSelector3").value = selectedElement.channels;
}

function unbindSelectedElement(){
    document.getElementById("elemAttribSelector1").value = "";
    document.getElementById("elemAttribSelector2").value = "";
    document.getElementById("elemAttribSelector3").value = "";
    selectedElement = null;
}

function bindDraggedElement(htmlElement){
    id = parseInt(htmlElement.id);
    draggedElement = elements[id];
}

function unbindDraggedElement(){
    draggedElement = null;
}

function bindSlot(newSelectedSlot){

    //the relevant JS Element object for the new selected slot stored in parent1
    let parent1 = elements[parseInt(newSelectedSlot.parentNode.id)];

    //Is the newSelectedslot input type and is it available?
    if(newSelectedSlot == parent1.slotInput && parent1.slotInputAvailable){
        if(selectedSlot.parentObj == null || selectedSlot.type == "input"){

            //First selection or choosing an input slot again
            selectedSlot.parentObj = elements[parseInt(newSelectedSlot.parentNode.id)];
            selectedSlot.elem = newSelectedSlot;
            selectedSlot.type = "input";
        }
        else{
            let translationTransform1 = getTranslationTransform(newSelectedSlot.parentNode);
            let translationTransform2 = getTranslationTransform(selectedSlot.elem.parentNode);

            //selectedSlot is the output slot, and newSelectedSlot is the input slot
            let x1 = newSelectedSlot.x.baseVal.value + slotWidth / 2 + translationTransform1.matrix.e;
            let y1 = newSelectedSlot.y.baseVal.value + slotHeight / 2 + translationTransform1.matrix.f;
            let x2 = selectedSlot.elem.x.baseVal.value + slotWidth / 2 + translationTransform2.matrix.e;
            let y2 = selectedSlot.elem.y.baseVal.value + slotHeight / 2 + translationTransform2.matrix.f;
            edges.push(new Edge(parseInt(selectedSlot.parentObj.id), parseInt(newSelectedSlot.parentNode.id), x2, y2, x1, y1));
            parent1.slotInputAvailable = false;
            selectedSlot.parentObj.slotOutputAvailable = false;
            //Deselect the currently selected slot
            selectedSlot.parentObj = null
            selectedSlot.elem = null;
        }
    }
    //or is the newSelectedSlot's type output and is it available?
    else if(newSelectedSlot == parent1.slotOutput && parent1.slotOutputAvailable){
        if(selectedSlot.parentObj == null || selectedSlot.type == "output"){

            //First selection or choosing an output slot again
            selectedSlot.parentObj = elements[parseInt(newSelectedSlot.parentNode.id)];
            selectedSlot.elem = newSelectedSlot;
            selectedSlot.type = "output";
        }
        else{
            let translationTransform1 = getTranslationTransform(newSelectedSlot.parentNode);
            let translationTransform2 = getTranslationTransform(selectedSlot.elem.parentNode);

            //selectedSlot is the input slot, and newSelectedSlot is the output slot
            let x1 = newSelectedSlot.x.baseVal.value + slotWidth / 2 + translationTransform1.matrix.e;
            let y1 = newSelectedSlot.y.baseVal.value + slotHeight / 2 + translationTransform1.matrix.f;
            let x2 = selectedSlot.elem.x.baseVal.value + slotWidth / 2 + translationTransform2.matrix.e;
            let y2 = selectedSlot.elem.y.baseVal.value + slotHeight / 2 + translationTransform2.matrix.f;
            edges.push(new Edge(parseInt(newSelectedSlot.parentNode.id), parseInt(selectedSlot.parentObj.id), x1, y1, x2, y2));
            parent1.slotOutputAvailable = false;
            selectedSlot.parentObj.slotInputAvailable = false;
        }
    }
}

function getTranslationTransform(theElement){
    let transforms = theElement.transform.baseVal;

    if (transforms.length === 0 || transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {
        // Create an transform that translates by (0, 0)
        let translate = svgWindow.createSVGTransform();
        translate.setTranslate(0, 0);
        theElement.transform.baseVal.insertItemBefore(translate, 0);
    }

    return transforms.getItem(0);
}

function makeDraggable(event){

    let offset, transform;

    function startDrag(event){
        if(event.target.classList.contains("slot")){
            bindSlot(event.target);
            return;
        }
        else if(event.target.parentNode != null && event.target.parentNode.classList.contains('draggable-group')){
            bindSelectedElement(event.target.parentNode);
            bindDraggedElement(event.target.parentNode);
        }
        else{
            if(event.target.id == "canvas"){
                console.log("unbinding selected element");
                unbindSelectedElement();
            }
            return;
        }

        offset = getMousePosition(svgWindow, event);

        // Get initial translation
        transform = getTranslationTransform(draggedElement.group);
        offset.x -= transform.matrix.e;
        offset.y -= transform.matrix.f;
    }

    function drag(event) {
        if (draggedElement != null) {
            event.preventDefault();
            let coordinates = getMousePosition(svgWindow, event);
            transform.setTranslate(coordinates.x - offset.x, coordinates.y - offset.y);

            //A variable to keep track of whether the edge is connected to the inputSlot or outputSlot
            //if true - inputSlot, if false - outputSlot
            let direction = false;

            let undirectedVertexList = undirectedGraph[draggedElement.id];
            let directedVertexList = directedGraph[draggedElement.id];

            for(let i = 0; i < undirectedVertexList.length; i++){
                let direction = false;
                for(j = 0; j < directedVertexList.length; j++){
                    if(undirectedVertexList[i] == directedVertexList[j]){
                        direction = true;
                        break;
                    }
                }

                let edgeID;
                if(direction){
                    edgeID = draggedElement.id + "-" + undirectedVertexList[i];
                }
                else{
                    edgeID = undirectedVertexList[i] + "-" + draggedElement.id;
                }

                for(j = 0; j < edges.length; j++){
                    if(edges[j].id === edgeID){
                        //if direction is true, the edge is connected to draggedElement's outputSlot, which means
                        //we should change the x1 y1 values of the edge.
                        let tt = getTranslationTransform(draggedElement.group);
                        if(direction){
                            let x1 = draggedElement.slotOutput.x.baseVal.value + slotWidth / 2 + tt.matrix.e;
                            let y1 = draggedElement.slotOutput.y.baseVal.value + slotHeight / 2 + tt.matrix.f;
                            edges[j].setPosition(x1, y1, edges[j].x2, edges[j].y2);
                        }
                        //otherwise we change the x2 y2 values of the edge
                        else{
                            let x2 = draggedElement.slotInput.x.baseVal.value + slotWidth / 2 + tt.matrix.e;
                            let y2 = draggedElement.slotInput.y.baseVal.value + slotHeight / 2 + tt.matrix.f;
                            edges[j].setPosition(edges[j].x1, edges[j].y1, x2, y2);
                        }
                    }
                }
            }
        }
    }

    function endDrag(event) {
        unbindDraggedElement();
    }
    svgWindow.addEventListener('mousedown', startDrag);
    svgWindow.addEventListener('mousemove', drag);
    svgWindow.addEventListener('mouseup', endDrag);
    svgWindow.addEventListener('mouseleave', endDrag);
    svgWindow.addEventListener('touchstart', startDrag);
    svgWindow.addEventListener('touchmove', drag);
    svgWindow.addEventListener('touchend', endDrag);
    //svgWindow.addEventListener('touchleave', endDrag);
    svgWindow.addEventListener('touchcancel', endDrag);
}

function changeParameter(event){
    let textInput = event.target;
    if(textInput.id == 'elemAttribSelector1' && selectedElement != null){
        selectedElement.kernelSize = textInput.value;
        sendElementChange(selectedElement.id);
    }
    else if(textInput.id == 'elemAttribSelector2' && selectedElement != null){
        selectedElement.stride = textInput.value;
        sendElementChange(selectedElement.id);
    }
    else if(textInput.id == 'elemAttribSelector3' && selectedElement != null){
        selectedElement.channels = textInput.value;
        sendElementChange(selectedElement.id);
    }
}

function removeEdge(event){
    if(event.target.classList.contains('edge')){
        let ID = event.target.id, i;
        for(i = 0; i < edges.length; i++){
            if(edges[i].id === ID){
                edges[i].theLine.remove();
                edges.splice(i, 1);
                break;
            }
        }

        //if all are in order, elementIDs should have 2 numbers as strings
        let elementIDs = ID.split("-");
        elements[parseInt(elementIDs[1])].slotInputAvailable = true;
        elements[parseInt(elementIDs[0])].slotOutputAvailable = true;

        removeFromList(undirectedGraph[parseInt(elementIDs[0])], parseInt(elementIDs[1]));
        removeFromList(undirectedGraph[parseInt(elementIDs[1])], parseInt(elementIDs[0]));
        removeFromList(directedGraph[parseInt(elementIDs[0])], parseInt(elementIDs[1]));
        //the Graph has changed: update it
        updateGraph();
    }
}

function removeFromList(theList, toRemove){
    let index = theList.indexOf(toRemove);
    if(index > -1){
        theList.splice(index, 1);
        return true;
    }
    throw new Error("Graph edge removal fail: does not exist");
}

svgWindow.addEventListener('mousedown', removeEdge);
svgWindow.addEventListener('load', makeDraggable);





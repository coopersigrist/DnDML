
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
            console.log("AAAA");
            //First selection or choosing an input slot again
            selectedSlot.parentObj = elements[parseInt(newSelectedSlot.parentNode.id)];
            selectedSlot.elem = newSelectedSlot;
            selectedSlot.type = "input";
        }
        else{
            console.log("BBBB");
            //selectedSlot is the output slot, and newSelectedSlot is the input slot
            let x1 = newSelectedSlot.x.baseVal.value + slotWidth / 2, y1 = newSelectedSlot.y.baseVal.value + slotHeight / 2;
            let x2 = selectedSlot.elem.x.baseVal.value + slotWidth / 2, y2 = selectedSlot.elem.y.baseVal.value + slotHeight / 2;
            edges.push(new Edge(parseInt(newSelectedSlot.parentNode.id), parseInt(selectedSlot.parentObj.id), x1, y1, x2, y2));
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
            console.log("CCCC");
            //First selection or choosing an output slot again
            selectedSlot.parentObj = elements[parseInt(newSelectedSlot.parentNode.id)];
            selectedSlot.elem = newSelectedSlot;
            selectedSlot.type = "output";
        }
        else{
            console.log("DDDD");
            //selectedSlot is the input slot, and newSelectedSlot is the output slot
            let x1 = newSelectedSlot.x.baseVal.value + slotWidth / 2, y1 = newSelectedSlot.y.baseVal.value + slotHeight / 2;
            let x2 = selectedSlot.elem.x.baseVal.value + slotWidth / 2, y2 = selectedSlot.elem.y.baseVal.value + slotHeight / 2;
            edges.push(new Edge(parseInt(selectedSlot.parentObj.id), parseInt(newSelectedSlot.parentNode.id), x2, y2, x1, y1));
            parent1.slotOutputAvailable = false;
            selectedSlot.parentObj.slotInputAvailable = false;
        }
    }
}

function makeDraggable(event){
    let svgWindow = event.target;

    let offset, transform;

    function startDrag(event){
        if(event.target.classList.contains("slot")){
            bindSlot(event.target);
            return;
        }
        else if(event.target.parentNode.classList.contains('draggable-group')){
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

        // Make sure the first transform on the element is a translate transform
        let transforms = draggedElement.group.transform.baseVal;

        if (transforms.length === 0 || transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {
            // Create an transform that translates by (0, 0)
            let translate = svgWindow.createSVGTransform();
            translate.setTranslate(0, 0);
            draggedElement.group.transform.baseVal.insertItemBefore(translate, 0);
        }

        // Get initial translation
        transform = transforms.getItem(0);
        offset.x -= transform.matrix.e;
        offset.y -= transform.matrix.f;
    }

    function drag(event) {
        if (draggedElement != null) {
            event.preventDefault();
            let coordinates = getMousePosition(svgWindow, event);
            transform.setTranslate(coordinates.x - offset.x, coordinates.y - offset.y);
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
    svgWindow.addEventListener('touchleave', endDrag);
    svgWindow.addEventListener('touchcancel', endDrag);
}

function changeParameter(event){
    let textInput = event.target;
    if(textInput.id == 'elemAttribSelector1' && selectedElement != null){
        selectedElement.kernelSize = textInput.value;
        updateBackend();
    }
    else if(textInput.id == 'elemAttribSelector2' && selectedElement != null){
        selectedElement.stride = textInput.value;
        updateBackend();
    }
    else if(textInput.id == 'elemAttribSelector3' && selectedElement != null){
        selectedElement.channels = textInput.value;
        updateBackend();
    }
}

svgWindow.addEventListener('load', makeDraggable);





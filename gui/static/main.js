
//selectElement is for keeping track of which Element's attribute should be changed, and draggedElement is
//for memoizing which element to drag.
let selectedElement = null, draggedElement = null;

//The directed graph will be send to the backend.
//need undirected graph to deal with keeping edges connected to elements that are being dragged around
let directedGraph = [], undirectedGraph = [];

let selectedSlot = {obj: null, elem: null, type: "input"};

var NS = "http://www.w3.org/2000/svg";

//the lists we are storing our Element and Edge objects in. Both objects have IDs which are stored in the JS object itself
//and HTML DOM element ID. The IDs correspond to the index at which they are stored in.
var elements = [], edges = [];

//the window we are drawing our elements in
let svgWindow = document.getElementsByClassName("svgArea")[0];
console.log(svgWindow);

// bind_selected_element(htmlElement: DOM): void
function bind_selected_element(htmlElement){
    id = parseInt(htmlElement.id);
    selectedElement = elements[id];
    document.getElementById("elemAttribSelector1").value = selectedElement.kernelSize;
    document.getElementById("elemAttribSelector2").value = selectedElement.stride;
    document.getElementById("elemAttribSelector3").value = selectedElement.channels;
}

// bind_selected_element(): void
function unbind_selected_element(){
    document.getElementById("elemAttribSelector1").value = "";
    document.getElementById("elemAttribSelector2").value = "";
    document.getElementById("elemAttribSelector3").value = "";
    selectedElement = null;
}

// bind_dragged_element(htmlElement: DOM): void
function bind_dragged_element(htmlElement){
    id = parseInt(htmlElement.id);
    draggedElement = elements[id];
}

// unbind_dragged_element(): void
function unbind_dragged_element(){
    draggedElement = null;
}

// bind_slot(newSelectedSlot: DOM): void
function bind_slot(newSelectedSlot){

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
            let translationTransform1 = get_translation_transform(newSelectedSlot.parentNode);
            let translationTransform2 = get_translation_transform(selectedSlot.elem.parentNode);

            //selectedSlot is the output slot, and newSelectedSlot is the input slot
            let x1 = newSelectedSlot.cx.baseVal.value + translationTransform1.matrix.e;
            let y1 = newSelectedSlot.cy.baseVal.value + translationTransform1.matrix.f;
            let x2 = selectedSlot.elem.cx.baseVal.value + translationTransform2.matrix.e;
            let y2 = selectedSlot.elem.cy.baseVal.value + translationTransform2.matrix.f;
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
            let translationTransform1 = get_translation_transform(newSelectedSlot.parentNode);
            let translationTransform2 = get_translation_transform(selectedSlot.elem.parentNode);

            //selectedSlot is the input slot, and newSelectedSlot is the output slot
            let x1 = newSelectedSlot.cx.baseVal.value + translationTransform1.matrix.e;
            let y1 = newSelectedSlot.cy.baseVal.value + translationTransform1.matrix.f;
            let x2 = selectedSlot.elem.cx.baseVal.value + translationTransform2.matrix.e;
            let y2 = selectedSlot.elem.cy.baseVal.value + translationTransform2.matrix.f;
            edges.push(new Edge(parseInt(newSelectedSlot.parentNode.id), parseInt(selectedSlot.parentObj.id), x1, y1, x2, y2));
            parent1.slotOutputAvailable = false;
            selectedSlot.parentObj.slotInputAvailable = false;
        }
    }
}





var selectedElementID = undefined;

let svg = document.getElementById("canvas");

function getMousePosition(svg, event) {
    var CTM = svg.getScreenCTM();
    if (event.touches) { event = event.touches[0]; }
    return {
        x: (event.clientX - CTM.e) / CTM.a,
        y: (event.clientY - CTM.f) / CTM.d
    };
}

function makeDraggable(event){
    let svg = event.target;

    let selectedElement, offset, transform;

    function startDrag(event){
        if(event.target.classList.contains('draggable')){
            selectedElement = event.target;
        }
        else if(event.target.parentNode.classList.contains('draggable-group')){
            selectedElement = event.target.parentNode;
            selectedElementID = selectedElement.id;
        }
        else{
            return;
        }
        console.log(selectedElement);
        offset = getMousePosition(svg, event);
    
        // Make sure the first transform on the element is a translate transform
        let transforms = selectedElement.transform.baseVal;
    
        if (transforms.length === 0 || transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {
            // Create an transform that translates by (0, 0)
            let translate = svg.createSVGTransform();
            translate.setTranslate(0, 0);
            selectedElement.transform.baseVal.insertItemBefore(translate, 0);
        }
    
        // Get initial translation
        transform = transforms.getItem(0);
        offset.x -= transform.matrix.e;
        offset.y -= transform.matrix.f;
    }
    
    function drag(event) {
        if (selectedElement) {
            event.preventDefault();
            let coordinates = getMousePosition(svg, event);
            transform.setTranslate(coordinates.x - offset.x, coordinates.y - offset.y);
        }
    }
    
    function endDrag(event) {
        selectedElement = false;
    }
    svg.addEventListener('mousedown', startDrag);
    svg.addEventListener('mousemove', drag);
    svg.addEventListener('mouseup', endDrag);
    svg.addEventListener('mouseleave', endDrag);
    svg.addEventListener('touchstart', startDrag);
    svg.addEventListener('touchmove', drag);
    svg.addEventListener('touchend', endDrag);
    svg.addEventListener('touchleave', endDrag);
    svg.addEventListener('touchcancel', endDrag);
}

function changeParameter(event){
    let textInput = event.target;
    console.log(textInput.id + " " + selectedElementID);
    let id = Number.parseInt(selectedElementID);
    if(textInput.id == 'elemAttribSelector1' && id != NaN){
        elements[id].kernelSize = textInput.value;
        updateBackend();
    }
    else if(textInput.id == 'elemAttribSelector2' && id != NaN){
        elements[id].stride = textInput.value;
        updateBackend();
    }
    else if(textInput.id == 'elemAttribSelector3' && id != NaN){
        elements[id].channels = textInput.value;
        updateBackend();
    }
}

svg.addEventListener('load', makeDraggable);





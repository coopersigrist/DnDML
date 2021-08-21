function make_draggable(event){

    let offset, transform;

    function start_drag(event){
        if(event.target.classList.contains("slot")){
            bind_slot(event.target);
            return;
        }
        else if(event.target.parentNode != null && event.target.parentNode.classList.contains('draggable-group')){
            bind_selectedElement(event.target.parentNode);
            bind_draggedElement(event.target.parentNode);
        }
        else{
            if(event.target.classList.contains("box-card-one")){
                console.log("unbinding selected element");
                unbind_selectedElement();
            }
            return;
        }

        offset = get_mouse_pos(svgWindow, event);

        // Get initial translation
        transform = get_translation_transform(draggedElement.group);
        offset.x -= transform.matrix.e;
        offset.y -= transform.matrix.f;
    }

    function drag(event) {
        if (draggedElement != null) {
            event.preventDefault();
            let coordinates = get_mouse_pos(svgWindow, event);
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
                        let tt = get_translation_transform(draggedElement.group);
                        if(direction){
                            let x1 = draggedElement.slotOutput.cx.baseVal.value + tt.matrix.e;
                            let y1 = draggedElement.slotOutput.cy.baseVal.value + tt.matrix.f;
                            edges[j].setPosition(x1, y1, edges[j].x2, edges[j].y2);
                        }
                        //otherwise we change the x2 y2 values of the edge
                        else{
                            let x2 = draggedElement.slotInput.cx.baseVal.value + tt.matrix.e;
                            let y2 = draggedElement.slotInput.cy.baseVal.value + tt.matrix.f;
                            edges[j].setPosition(edges[j].x1, edges[j].y1, x2, y2);
                        }
                    }
                }
            }
        }
    }

    function end_drag(event) {
        unbind_draggedElement();
    }
    svgWindow.addEventListener('mousedown', start_drag);
    svgWindow.addEventListener('mousemove', drag);
    svgWindow.addEventListener('mouseup', end_drag);
    svgWindow.addEventListener('mouseleave', end_drag);
    svgWindow.addEventListener('touchstart', start_drag);
    svgWindow.addEventListener('touchmove', drag);
    svgWindow.addEventListener('touchend', end_drag);
    //svgWindow.addEventListener('touchleave', end_drag);
    svgWindow.addEventListener('touchcancel', end_drag);
}

svgWindow.addEventListener('load', make_draggable);

//listener for setting up the parameters of elements
function parameter_changed(event){
    let textInput = event.target;
    if(textInput.id == 'elemAttribSelector1' && selectedElement != null){
        selectedElement.kernelSize = textInput.value;
        send_elem_change(selectedElement.id);
    }
    else if(textInput.id == 'elemAttribSelector2' && selectedElement != null){
        selectedElement.stride = textInput.value;
        send_elem_change(selectedElement.id);
    }
    else if(textInput.id == 'elemAttribSelector3' && selectedElement != null){
        selectedElement.channels = textInput.value;
        send_elem_change(selectedElement.id);
    }
}
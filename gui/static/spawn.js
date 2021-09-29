//Draws the correct elements and appendChild them all to group
// element_svg_config(group: DOM, type: string): DOM[3]
function element_svg_config(group, type){
    //This list will be returned to return the group and slot variables.
    let toReturn = [];
    if(type == "data"){
        let dataPath1 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
        dataPath1.setAttribute("d", "M2 21.3071C2 10.6769 13.1929 2 27 2C40.8071 2 52 10.6769 52 21.3071" +
            "V34.5V47.6929C52 58.3559 40.8071 67 27 67C13.1929 67 2 58.3559 2 47.6929V34.5V21.3071Z");
        dataPath1.setAttribute("fill", "#E2E6FB");

        let dataPath2 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
        dataPath2.setAttribute("d", "M52 21.3071C52 31.9373 40.8071 40.6142 27 40.6142C13.1929 40.6142 2 31.9373 2 21.3071M52 21.3071C52 10.6769 40.8071 2 27 2C13.1929 2 2 10.6769 2 21.3071M52 21.3071V34.5M2 21.3071V34.5M52 34.5C52 45.163 40.8071 53.8071 27 53.8071C13.1929 53.8071 2 45.163 2 34.5M52 34.5V47.6929C52 58.3559 40.8071 67 27 67C13.1929 67 2 58.3559 2 47.6929V34.5");
        dataPath2.setAttribute("stroke", "black");
        dataPath2.setAttribute("stroke-width", "3.5");
        dataPath2.style.fill = "none";

        let slotInput = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
        slotInput.classList.add("slot");
        slotInput.setAttribute("cx", "-5");
        slotInput.setAttribute("cy", "35");
        slotInput.setAttribute("r", "3");
        slotInput.setAttribute("fill", "black");

        let slotOutput = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
        slotOutput.classList.add("slot");
        slotOutput.setAttribute("cx", "60");
        slotOutput.setAttribute("cy", "35");
        slotOutput.setAttribute("r", "3");
        slotOutput.setAttribute("fill", "black");

        group.appendChild(dataPath1);
        group.appendChild(dataPath2);
        group.appendChild(slotInput);
        group.appendChild(slotOutput);

        toReturn.splice(0, 0, group, slotInput, slotOutput);
    }
    // else if(type == "convolution"){
    //     let convolutionPath1 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
    //     convolutionPath1.setAttribute("d", "M73.75 25.5V70.75C73.75 72.4069 72.4069 73.75 70.75 73.75 " +
    //         "H25.5C23.8431 73.75 22.5 72.4069 22.5 70.75V63.5H15.25C13.5931 63.5 12.25 62.1569 12.25 60.5 " +
    //         "V53.25H5C3.34315 53.25 2 51.9069 2 50.25V43V5C2 3.34315 3.34315 2 5 2H43H50.25 " +
    //         "C51.9069 2 53.25 3.34315 53.25 5V12.25H60.5C62.1569 12.25 63.5 13.5931 63.5 15.25 " +
    //         "V22.5H70.75C72.4069 22.5 73.75 23.8431 73.75 25.5Z");
    //     convolutionPath1.setAttribute("fill", "#DAE3F8");
    //     let convolutionPath2 = document.createElementNS("http://www.w3.org/2000/svg", 'path');
    //     convolutionPath2.setAttribute("d", d="M53.25 12.25H15.25C13.5931 12.25 12.25 13.5931 12.25 15.25 " +
    //         "V53.25M53.25 12.25H60.5C62.1569 12.25 63.5 13.5931 63.5 15.25V22.5M53.25 12.25V5" +
    //         "C53.25 3.34315 51.9069 2 50.25 2H43H5C3.34315 2 2 3.34315 2 5V43V50.25C2 51.9069 3.34315 53.25 5 53.25" +
    //         "H12.25M12.25 53.25V60.5C12.25 62.1569 13.5931 63.5 15.25 63.5H22.5M63.5 22.5H70.75" +
    //         "C72.4069 22.5 73.75 23.8431 73.75 25.5V70.75C73.75 72.4069 72.4069 73.75 70.75 73.75H25.5" +
    //         "C23.8431 73.75 22.5 72.4069 22.5 70.75V63.5M63.5 22.5H25.5C23.8431 22.5 22.5 23.8431 22.5 25.5V63.5");
    //     convolutionPath2.setAttribute("stroke", "black");
    //     convolutionPath2.setAttribute("stroke-width", "4");

    //     group.appendChild(convolutionPath1);
    //     group.appendChild(convolutionPath2);
    // }
    
    return toReturn;
}

class Element{
    static highestID = 0;

    constructor(x, y){
        let type = "data";
        this.id = Element.highestID++;
        this.x = x;
        this.y = y;
        this.kernelSize = '';
        this.stride = '';
        this.channels = '';

        this.group = document.createElementNS(NS, 'g');
        this.group.classList.add('draggable-group');
        this.group.id = (Element.highestID - 1).toString() + " element";

        let groupAndSlots = element_svg_config(this.group, type);
        this.group = groupAndSlots[0];
        this.slotInput = groupAndSlots[1];
        this.slotOutput = groupAndSlots[2];

        //Keeping track of whether the slot can be used to draw an edge or not
        this.slotInputAvailable = true;
        this.slotOutputAvailable = true;
    }
    draw(svg){
        svg.appendChild(this.group);
    }
    toJSON(){
        return{
            id: this.id,
            type: "element",
            kernelSize: this.kernelSize,
            stride: this.stride,
            channels: this.channels
        }
    }
    setKernelSize(kernelSize){
        this.kernelSize = kernelSize;
    }
    setStride(stride){
        this.stride = stride;
    }
    setChannels(channels){
        this.channels = channels;
    }
}

// spawnElem(event: Event): void
function spawnElem(event){
    let svgWindow = document.getElementsByClassName("box-card-one")[0];
    if(event.which == 2){
        let pos = get_mouse_pos(svgWindow, event);
        spawnElemHelper(svgWindow, pos.x, pos.y);
    }
}

// spawnElemHelper()
function spawnElemHelper(svg, x, y){
    topLeft = {x: x,
               y: y};
    let newElement = new Element(topLeft.x, topLeft.y);
    elements.push(newElement);

    send_elem_creation(newElement.id);
    undirectedGraph[newElement.id] = [];
    directedGraph[newElement.id] = [];

    newElement.draw(svg);
}

document.getElementsByClassName('box-card-one')[0].addEventListener('mousedown', spawnElem);

class Edge{
    //groupID1, x1, y1 belongs to output slot and groupID2, x2, y2 belongs to input slot
    constructor(groupID1, groupID2, x1, y1, x2, y2){
        directedGraph[groupID1].push(groupID2);
        undirectedGraph[groupID1].push(groupID2);
        undirectedGraph[groupID2].push(groupID1);
        //the Graph has changed: update it
        update_graph();

        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;

        this.id = groupID1.toString() + "-" + groupID2.toString();

        this.theLine = document.createElementNS("http://www.w3.org/2000/svg", 'line');
        this.theLine.classList.add("edge");
        this.theLine.id = groupID1.toString() + "-" + groupID2.toString();
        this.theLine.setAttribute("x1", x1);
        this.theLine.setAttribute("x2", x2);
        this.theLine.setAttribute("y1", y1);
        this.theLine.setAttribute("y2", y2);

        svgWindow.appendChild(this.theLine);
    }

    setPosition(x1, y1, x2, y2){
        this.x1 = x1;
        this.y1 = y1;
        this.x2 = x2;
        this.y2 = y2;

        this.theLine.setAttribute("x1", x1);
        this.theLine.setAttribute("x2", x2);
        this.theLine.setAttribute("y1", y1);
        this.theLine.setAttribute("y2", y2);
    }
}

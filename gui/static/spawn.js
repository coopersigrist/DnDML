
class Element{
    static highestID = 0;

    constructor(x, y){
        this.id = Element.highestID++;
        this.x = x;
        this.y = y;
        this.kernelSize = '';
        this.stride = '';
        this.channels = '';

        this.group = document.createElementNS(NS, 'g');
        this.group.classList.add('draggable-group');
        this.group.id = (Element.highestID - 1).toString() + " element";

        this.main = document.createElementNS("http://www.w3.org/2000/svg", 'rect');
        this.main.setAttribute('x', x.toString());
        this.main.setAttribute('y', y.toString());
        this.main.setAttribute('width', elemWidth.toString());
        this.main.setAttribute('height', elemHeight.toString());
        this.main.setAttribute('fill', 'blue');

        this.slotInput = document.createElementNS(NS, 'rect');
        this.slotInput.classList.add("slot");
        this.slotInput.setAttribute('x', x.toString());
        this.slotInput.setAttribute('y', (y + (elemHeight - slotHeight) / 2).toString());
        this.slotInput.setAttribute('width', slotWidth.toString());
        this.slotInput.setAttribute('height', slotHeight.toString());
        this.slotInput.setAttribute('fill', 'yellow');

        this.slotOutput = document.createElementNS(NS, 'rect');
        this.slotOutput.classList.add("slot");
        this.slotOutput.setAttribute('x', (x + elemWidth - slotWidth).toString());
        this.slotOutput.setAttribute('y', (y + (elemHeight - slotHeight) / 2).toString());
        this.slotOutput.setAttribute('width', slotWidth.toString());
        this.slotOutput.setAttribute('height', slotHeight.toString());
        this.slotOutput.setAttribute('fill', 'yellow');

        this.group.appendChild(this.main);
        this.group.appendChild(this.slotInput);
        this.group.appendChild(this.slotOutput);

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

function spawnElem(event){
    let svgWindow = document.getElementById("canvas");
    if(event.which == 2){
        let pos = get_mouse_pos(svgWindow, event);
        spawnElemHelper(svgWindow, pos.x, pos.y);
    }
}

function spawnElemHelper(svg, x, y){
    topLeft = {x: x - elemWidth / 2,
               y: y - elemHeight / 2
            };
    let newElement = new Element(topLeft.x, topLeft.y);
    elements.push(newElement);

    send_elem_creation(newElement.id);
    undirectedGraph[newElement.id] = [];
    directedGraph[newElement.id] = [];

    newElement.draw(svg);
}

document.getElementById('canvas').addEventListener('mousedown', spawnElem);

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

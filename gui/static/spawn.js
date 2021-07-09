
var NS = "http://www.w3.org/2000/svg", elemWidth = 80, elemHeight = 40, slotWidth = 10, slotHeight = 10;
var elements = [];

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
    }
    draw(svg){
        svg.appendChild(this.group);
    }
    toJSON(){
        Element.highestID++;
        return{
            id: this.id,
            type: "element",
            x: this.x,
            y: this.y,
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
    let svg = document.getElementById("canvas");
    if(event.which == 3){
        let pos = getMousePosition(svg, event)
        spawnElemHelper(svg, pos.x, pos.y);
    }
}

function spawnElemHelper(svg, x, y){
    topLeft = {x: x - elemWidth / 2,
               y: y - elemHeight / 2
            };
    let newElement = new Element(topLeft.x, topLeft.y);
    elements.push(newElement);
    selectedElementID = newElement.id;
    updateBackend();

    newElement.draw(svg);
}

function updateBackend(){
    fetch('/', {

        // Declare what type of data we're sending
        headers: {
          'Content-Type': 'application/json'
        },

        // Specify the method
        method: 'POST',

        // A JSON payload
        body: JSON.stringify(elements)
    }).then(function (response) { // At this point, Flask has printed our JSON
        return response.text();
    }).then(function (text) {

        console.log('POST response: ');

        // Should be 'OK' if everything was successful
        console.log(text);
    });
}

document.getElementById('canvas').addEventListener('mousedown', spawnElem);




import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function get_mouse_pos(svgWindow, event) {
    var CTM = svgWindow.getScreenCTM();
    if (event.touches) { event = event.touches[0]; }
    return {
        x: (event.clientX - CTM.e) / CTM.a,
        y: (event.clientY - CTM.f) / CTM.d
    };
}

class NavButton extends React.Component {
    render() {
        return (<a className={this.props.active ? "active" : ""}
                onClick={() => this.props.onClick(this.props.tag)}>
            {this.props.tag}
        </a>)
    }
}
class NavBar extends React.Component {
    renderButton(tag, activepage) {
        return (<NavButton tag={tag} 
            active={activepage === tag}
            onClick={(tag) => this.props.onClick(tag)}>
        </NavButton>)
    }
    render() {
        return (<nav className={"navbar"}>
            {this.renderButton("Model", this.props.activepage)}
            {this.renderButton("Dataset", this.props.activepage)}
            {this.renderButton("Training", this.props.activepage)}
            {this.renderButton("Testing", this.props.activepage)}
            {this.renderButton("Tuning", this.props.activepage)}
            <img id="theme-toggle" src="./Assets/Light.svg" alt="UI theme toggle button"/>
        </nav>);
    }
}

class Component extends React.Component {
    constructor(props) {
        super(props);
        let bodyPart1= <path xmlns={this.props.NS} 
            d={"M2 21.3071C2 10.6769 13.1929 2 27 2C40.8071 2 52 10.6769 52 21.3071 V34.5V47.6929C52 58.3559 40.8071 67 27 67C13.1929 67 2 58.3559 2 47.6929V34.5V21.3071Z"}
            fill={"#E2E6FB"}>
        </path>;
        let bodyPart2 = <path xmlns={this.props.NS} 
            d={"M52 21.3071C52 31.9373 40.8071 40.6142 27 40.6142C13.1929 40.6142 2 31.9373 2 21.3071M52 21.3071C52 10.6769 40.8071 2 27 2C13.1929 2 2 10.6769 2 21.3071M52 21.3071V34.5M2 21.3071V34.5M52 34.5C52 45.163 40.8071 53.8071 27 53.8071C13.1929 53.8071 2 45.163 2 34.5M52 34.5V47.6929C52 58.3559 40.8071 67 27 67C13.1929 67 2 58.3559 2 47.6929V34.5"}
            stroke={"black"}
            stoke-width={"3.5"}
            fill={"none"}>
        </path>;
        let inputSlot = <circle xmlns={this.props.NS}
            className={"slot"}
            cx={"-5"}
            cy={"35"}
            r={"3"}
            fill={"black"}>
        </circle>;
        let outputSlot = <circle xmlns={this.props.NS}
            className={"slot"}
            cx={"60"}
            cy={"35"}
            r={"3"}
            fill={"black"}>
        </circle>;

        this.state = {
            id: this.props.id,
            group: <g className="draggable">
                {bodyPart1}
                {bodyPart2}
                {inputSlot}
                {outputSlot}
            </g>,
        };
    }

    render(){
        return this.state.group;
    }
}
class MainArea extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            directedGraph: [],
            undirectedGraph: [],
            selectedElement: undefined,
            draggedElement: undefined,
            NS: "http://www.w3.org/2000/svg",
            components: [],
            edges: [],
            highestID: 0,
        };
    }
    addComponent(x, y){
        this.setState({

        });
    }

    handleClick(event) {
        //alert(event.target.classList);
        if (event.target.classList.contains("svgArea")) {
            //alert("FF");
            let newComponents = this.state.components.slice();
            //if(event.buttons === 1){
                let pos = get_mouse_pos(event.target, event);
                newComponents.push(<Component NS={this.state.NS} 
                    x={pos.x}
                    y={pos.y}>
                </Component>);
            //}
            this.setState({
                directedGraph: this.state.directedGraph,
                undirectedGraph: this.state.undirectedGraph,
                selectedElement: this.state.selectedElement,
                draggedElement: this.state.draggedElement,
                NS: this.state.NS,
                components: newComponents,
                edges: this.state.edges,
                highestID: this.state.highestID,
            });
        }
    }
    render(){
        let toDraw = [];
        for (let i = 0; i < this.state.components.length; ++i) {
            toDraw.push(this.state.components[i]);
        }
        for (let i = 0; i < this.state.edges.length; ++i) {
            toDraw.push(this.state.edges[i]);
        }
        return (<svg
            className = "svgArea" width="400" height="400"
            viewBox="0 0 400 400" fill="none"
            xmlns="http://www.w3.org/2000/svg"
            onClick={(event)=>this.handleClick(event)}>
                {toDraw}
          </svg>);
    }
}
class ModelVerticalBar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

        };
    }
}

class ModelPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            
        };
    }
    render() {
        let modelPage = [];
        let mainArea = <MainArea type={"Model"}></MainArea>;
        modelPage.push(mainArea);
        return modelPage;
    }
}

class App extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            currPage: "Model"
        };
    }

    handleNavBar(tag) {
        this.setState({
            currPage: tag
        });
    }
    render() {
        let wholePage = [];
        const navBar = (<NavBar activepage={this.state.currPage} onClick={(tag) => this.handleNavBar(tag)}></NavBar>);
        const modelPage = (<ModelPage></ModelPage>);
        wholePage.push(navBar);
        if(this.state.currPage === "Model")wholePage.push(modelPage);
        return <div>{wholePage}</div>;
    }
}

document.body.classList.add("light");
ReactDOM.render(<App />, document.getElementById('root'));
  
  
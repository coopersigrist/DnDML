function changeBodyColor(){
    let bodyElem = document.getElementById("body");
    if(bodyElem.style["background-color"] == "red"){
        bodyElem.style["background-color"] = "aqua"
    }
    else{
        bodyElem.style["background-color"] = "red"
    }
}

function calcSqrt(){
    let inputNum = 0 + parseInt(document.getElementsByClassName("textbox")[0].value);
    if(Number.isNaN(inputNum)){
        document.getElementsByClassName("output")[0].innerHTML = "A number could not be extracted from the text you have provided";
    }
    else{
        let sqrtNum = Math.sqrt(inputNum);
        sqrtNum = sqrtNum.toFixed(2);
        document.getElementsByClassName("output")[0].innerHTML = "The square root of " + inputNum.toString() + " is: <br>" + sqrtNum.toString();
    }
}
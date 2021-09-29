// remove_edge(event: Event): void
function remove_edge(event){
    if(event.target.classList.contains('edge')){
        let ID = event.target.id, i;
        //remove the appropiate edge by first deleteing the DOM object, then removing it from edges.
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

        remove_from_list(undirectedGraph[parseInt(elementIDs[0])], parseInt(elementIDs[1]));
        remove_from_list(undirectedGraph[parseInt(elementIDs[1])], parseInt(elementIDs[0]));
        remove_from_list(directedGraph[parseInt(elementIDs[0])], parseInt(elementIDs[1]));
        //the Graph has changed: update it
        update_graph();
    }
}
svgWindow.addEventListener('mousedown', remove_edge);

//Attemps to remove soemthing from a list.
// remove_from_list(theList: number[], toRemove: number): boolean
function remove_from_list(theList, toRemove){
    let index = theList.indexOf(toRemove);
    if(index > -1){
        theList.splice(index, 1);
        return true;
    }
    throw new Error("List removal fail: does not exist");
}
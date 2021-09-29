//gets the transform(translation type) of any elemnt
function get_translation_transform(theElement){
    let transforms = theElement.transform.baseVal;

    if (transforms.length === 0 || transforms.getItem(0).type !== SVGTransform.SVG_TRANSFORM_TRANSLATE) {
        // Create an transform that translates by (0, 0) if there isn't one already created
        let translate = svgWindow.createSVGTransform();
        translate.setTranslate(0, 0);
        theElement.transform.baseVal.insertItemBefore(translate, 0);
    }

    return transforms.getItem(0);
}

//get mouse position within the context of the svgWindow
function get_mouse_pos(svgWindow, event) {
    var CTM = svgWindow.getScreenCTM();
    if (event.touches) { event = event.touches[0]; }
    return {
        x: (event.clientX - CTM.e) / CTM.a,
        y: (event.clientY - CTM.f) / CTM.d
    };
}
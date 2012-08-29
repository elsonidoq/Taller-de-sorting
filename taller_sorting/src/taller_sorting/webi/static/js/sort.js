var SortAlgorithm = function Player(container) {
    this.container= container
}

SortAlgorithm.prototype.update= function(data) {
    this.container.children().remove();
    
    var height= this.container.height();
    var line_height= (height - data.length)/data.length;
    if(line_height != parseInt(line_height)) {
        line_height= parseInt(line_height+1);
        height= (line_height+1)*data.length;
        this.container.height(height);
    }
    var width= this.container.width();

    this.max_value= 0;
    for(var i in data) {
        this.max_value= Math.max(this.max_value, data[i][0]);
    }

    for(var i in data) {
        var css= {'height':line_height + 'px', 
                  'width':width*data[i][0]/this.max_value + 'px'} 
        if(data[i].length == 2) {
            for(var j in data[i][1]) {
                css[j]= data[i][1][j];
            }
        }
        var line= $("<div>").addClass("sorting-line")
                            .css(css)
                            .appendTo(this.container)
                            .attr('id', 'line_' + i);

        var separator= $("<div>").css({'height':'1px'})
                                 .appendTo(this.container);
    }
        

}


SortAlgorithm.prototype.clear_colors= function() {
    this.container.find(".sorting-line").css("background", "");
}

SortAlgorithm.prototype.single_update= function(position, color, value) {
    this.container.find(".sorting-line").css("background", "");
    this.container.find("#line_" + position).css("background", color);
    if(value) {
        this.container.find("#line_" + position).css("width", this.container.width()*value/this.max_value);
    }

}


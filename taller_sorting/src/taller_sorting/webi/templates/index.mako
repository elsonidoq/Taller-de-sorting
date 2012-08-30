<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <title> Taller de sorting</title>
	<script type="text/javascript" src="/js/jquery.js"></script>
	<script type="text/javascript" src="/js/jquery-ui.js"></script>
	<script type="text/javascript" src="/js/sort.js"></script>
    
    <link type="text/css" href="/css/jquery-ui-1.8.23.custom.css" rel="stylesheet" /> 
    
    
	<script type="text/javascript" src="/js/jquery.ui.core.js"></script> 
	<script type="text/javascript" src="/js/jquery.ui.widget.js"></script> 
	<script type="text/javascript" src="/js/jquery.ui.mouse.js"></script> 
	<script type="text/javascript" src="/js/jquery.ui.slider.js"></script> 

    <style>
        .sorting-line {
            background: #ccc;
        }

        .visualization-container {

            border:solid 1px; 
            height:150px; 
            width:150px
        }
        
        .top-bar-description {
            text-align:center;
            font-size:12px;

        }
    </style>
    <script type="text/javascript">
    function resize() {
/*        var tbc= $("#top-bar-content");
        var width= tbc.width();
//        tbc.children().each(function(p,e){width+=$(e).width()})
        tbc.css({'margin-left': ($("#top-bar").width() - width)/2 + "px"});*/

    }
    $(document).ready(function(){
        $("#speed-slider").slider({
                min:1, 
                max:50, 
                step:1,
                value:10,
                change:function(event, ui){
                    $("#speed-slider-text").text(ui.value); 
                }});
        $("#size-slider").slider({
                min:2, 
                max:100, 
                value:50,
                step:2,
                change:function(event, ui){
                    $("#size-slider-text").text(ui.value); 
                    if(!is_sorting || (is_sorting && is_paused)) { get_implementations();}
                }});
        $("#speed-slider-text").text($("#speed-slider").slider("value")); 
        $("#size-slider-text").text($("#size-slider").slider("value")); 

        $("#algorithms_selection").dialog({title:"selecci&oacute;n de algoritmos", minWidth:700, autoOpen:false});
        get_implementations();
        $(window).resize(resize);
    });

    var puesto= 0;
    var group_updates= null;
    var sorting_algorithms= [];
    var finished= 0;
    var is_sorting= false;
    var is_paused= false;
    
    function load_visualizations(values, group_names) {
        $("#visualizations").children().remove();
        sorting_algorithms= [];
        for(var i in group_names) {
            var name= group_names[i];
            
            var container= $("<div>").appendTo("#visualizations")
                                     .css({'float':'left', 'margin':'10px'});

            $("<span>").appendTo(container)
                     .text(name)
                     .attr('id', 'group_' + i)
                     .css({'font-size':'12px', 'margin-right':'10px'});

            $("<span>").appendTo(container)
                       .attr('id', 'group_position_' + i);
                       

            var vis_container= $("<div>").appendTo(container)
                                         .addClass("visualization-container");
            
            container.show();

            var s= new SortAlgorithm(vis_container);
            s.update(values);
            sorting_algorithms.push(s)
        }

    }
    
    function algorithm_onchange() {
        var algorithm= $("#algorithm").val();
        if(algorithm == 'custom'){
            $('#algorithms_selection').dialog('open');
        } else {
            get_implementations();
        }

    }

    function get_implementations() {
        if(is_sorting && !is_paused) return;
        is_sorting= false; is_paused= false;
        var algorithm= $("#algorithm").val();
        
        var custom_algorithms= null;
        if(algorithm == 'custom'){
            custom_algorithms= get_selected_algorithms().join(',');
        }

        var data= {'algorithm':algorithm, 
                   'custom_algorithms':custom_algorithms,
                   'size':$("#size-slider").slider("value"),
                   'order':$("#order").val()};
        
        $.ajax({url:'get_implementations',
                data:data,
                success:function(data) {
                    load_visualizations(data[0], data[1]);
                }
        });
    }
    
    function pause_sorting() {
        is_paused= true;
        $("#play").show();
        $("#pause").hide();
    }

    function start_sorting() {
        if(!is_paused) {
            finished= 0;
            var algorithm= $("#algorithm").val();
            var custom_algorithms= null;
            if(algorithm == 'custom'){
                custom_algorithms= get_selected_algorithms().join(',');
            }
            var data= {'algorithm':algorithm, 
                       'custom_algorithms':custom_algorithms,
                       'size':$("#size-slider").slider("value"),
                       'order':$("#order").val()};

            $("#visualizations").children().remove();
            $("#wait").show("slide", {direction:"up"});
            $.ajax({url:'start_sorting',
                    data:data,
                    success:function(data) {
                        $("#wait").hide("slide", {direction:"up"}, callback=function() {
                            load_visualizations(data[0], data[1]);
                            
                            group_updates= data[2];
                            do_sort();
                            $("#play").hide();
                            $("#pause").show();
                            
                        });
                    }
            });
        } else {
            is_paused= false;
            do_sort();
            $("#play").hide();
            $("#pause").show();
        }
    }

    function do_sort() {
        is_sorting= true;
        var has_to_continue= false;
        var finished_groups= []
        for(var i in group_updates) {
            var l= group_updates[i];
            if(l.length > 0) {
                var content= l[0];
                if(content != 'cmp' && content != 'crash') {
                    sorting_algorithms[i].single_update(l[0][0], l[0][1], l[0][2]);
                }
                l.splice(0,1);
                has_to_continue= has_to_continue || l.length > 0;
                if(l.length == 0) {
                    if (content == 'crash') {
                        $('#group_' + i).css({'color':'#C00'});
                    } else {
                        $('#group_' + i).css({'color':'#0C0'});
                        finished_groups.push(i);
                    }
                    sorting_algorithms[i].clear_colors();
                }
            }
        }

        for(var i in finished_groups) {
            $("#group_position_" + finished_groups[i]).text(finished+1);
        }
        if(finished_groups.length > 0) finished++;
        if(has_to_continue && !is_paused) {
            var interval= $("#speed-slider").slider("value");
            setTimeout("do_sort();", interval);
        } else if (!is_paused){
            is_sorting= false;
            is_paused= false;
            $("#play").show();
            $("#pause").hide();
        }
    }


    function get_selected_algorithms() {
        var checked= $("#algorithms_selection input:checked").get();
        var l=[];
        for(var i in checked) {
            l.push($(checked[i]).attr('algorithm_id'));
        }
        return l;
    }

    function select_all() {
        $("#algorithms_selection input").attr('checked',true);
    }

    function select_none() {
        $("#algorithms_selection input").attr('checked',false);
    }
    

    </script>
</head>
<body style="margin:0 auto;" onload="javascript:resize();">
    <div id="algorithms_selection" style="display:none">
        <div style="text-align:right;font-size:10px">
            <a href="#" onclick="javascript:select_all()">seleccionar todos</a>
            <a href="#" onclick="javascript:select_none()">seleccionar ninguno</a>
            <a href="#" onclick="javascript:get_implementations();$('#algorithms_selection').dialog('close');">aceptar</a>
        </div>
        % for group_name, group_algorithms in algorithms_per_group.iteritems():
            <div>
                <h3>${group_name}</h3>
                <div style="margin-left:20px">
                    % for algorithm in group_algorithms:
                        <div style="font-size:80%; margin:5px 20px;float:left"><input algorithm_id="${group_name}/${algorithm}" type="checkbox"/>${algorithm}</div>
                    % endfor
                </div>
            </div>
            <div style="clear:both"></div>
        % endfor
        <div style="text-align:right"><a href="#" onclick="javascript:get_implementations();$('#algorithms_selection').dialog('close');">aceptar</a></div>
    </div>

    <div style="margin: 0px 15px">
        <div id="top-bar" style="float: right; left: -50%; position: relative; text-align: left;">
        
            <div id="top-bar-content">
                <ul style="left: 50%; list-style: none; margin: 0px; padding: 0px; position: relative;">
                <li style="float:left;margin:0px 20px;position:relative;" >
                    <img id="play" style="cursor:pointer;" src='/images/play.png' onclick="javascript:start_sorting();"/>
                    <img id="pause" style="display:none;cursor:pointer;" src='/images/pause.png' onclick="javascript:pause_sorting();"/>
                </li>
                <li style="float:left; position:relative; margin-right:20px; margin-top:15px" > 
                    <div class="top-bar-description" >Algoritmo: </div>
                        <div> <select id="algorithm" onchange="javascript:algorithm_onchange();" >
                            % for algorithm in sorted(all_algorithms):
                                <option value="${algorithm}">${algorithm}</option>
                            % endfor
                            <option value="custom">Custom</option>
                           </select>
                        </div>
                </li>
                <li style="position:relative;float:left;margin:15px 10px 20px 0">
                    <div class="top-bar-description" style="margin-bottom:3px" >Tama&ntilde;o <span style="font-size:10px">(<span id="size-slider-text"></span>)</span></div>
                    <div id="size-slider" style=";float:left;width:200px"></div>
                </li>
                <li style="float:left;margin:15px 10px 20px 10px">
                    <div class="top-bar-description" style="margin-bottom:3px" >Refresco <span style="font-size:10px">(<span id="speed-slider-text"></span>)</span></div>

                    <div id="speed-slider" style="float:left;width:100px"></div>
                </li>

                <li style="float:left;margin:15px 0" >
                    <div class="top-bar-description">Caso: </div>
                    <div> <select id="order" onchange="javascript:algorithm_onchange();"> 
                                   <option value="random">Aleatorio</option>
                                   <option value="almost-sorted">Casi ordenado</option>
                                   <option value="asc">Ascendente</option>
                                   <option value="desc">Descendente</option>
                          </select>                                </div>
                </li>
                </ul>
            </div>                

            <div style="clear:both"></div>
        </div>
        <div style="width:100%;height:1px;clear:both;border-bottom:solid 1px;"></div>
        <div id="wait" style="widht:100%;text-align:center; display:none; margin: 10px 10px" >Espera...</div>

        <div id="visualizations">

        </div>

    </div>
    <script type="text/javascript">
        
    </script>
</body>
</html>

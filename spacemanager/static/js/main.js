fslm = {
    queues: {
        collapse: function(drive) { 
                $('tr#'+drive).not('.newDrive').hide(300);
                $('tr#' + drive + '.newDrive').find('td').eq(0).html('+');
                $('tr#' + drive + '.newDrive').find('td').eq(0).attr('onclick','fslm.queues.expand(\''+drive+'\')');
                return;
            },
            expand: function(drive) { 
                $('tr#'+drive).not('.newDrive').show(300);
                $('tr#' + drive + '.newDrive').find('td').eq(0).html('-');
                $('tr#' + drive + '.newDrive').find('td').eq(0).attr('onclick','fslm.queues.collapse(\''+drive+'\')');
                return;
            }
    },
drives : {
	sizeData : {},
	getDrivesSize: function(callback){
	  $.get('/driveslist',function(data) {
		eval('fslm.drives.sizeData = ' + data)
		if (callback != null)
		{
			callback();
		}
		})
	},
	drawDrives: function(){
         $('#loader').remove();
		 for (i=0;i<fslm.drives.sizeData.length;i++) {
			fslm.drives.drawDrive(fslm.drives.sizeData[i],i);
			 //alert(fslm.drives.sizeData[i].name);
			}
	},
    drawDrive: function(drve, index) {
			 //var x = index*fslm.drives.drawXPadding + index*fslm.drives.drawWidth + fslm.drives.drawXPadding;
             var x = fslm.drives.drawXPadding ;
             var y = index*fslm.drives.drawYPadding + index*fslm.drives.drawHeight + fslm.drives.drawYPadding;
			 var drive = fslm.paper.rect(x-1,y-1,fslm.drives.drawWidth+2,fslm.drives.drawHeight+2);
             drive.click(function() { document.location= drve.link });
			 drive.attr({stroke:"#333333","stroke-width":2,fill: "#FFF","font-size":fslm.drives.drawFontSize,cursor:"pointer"});
             var percentage = (drve.used/ drve.capacity) ;
             var driveFull = fslm.paper.rect(x,y,fslm.drives.drawWidth*percentage,fslm.drives.drawHeight);
             driveFull.click(function() { document.location= drve.link });
             driveFull.attr({stroke:"none","stroke-width":"0",cursor:"pointer"});
             if (drve.isOver == "False")
             {
                driveFull.attr({fill:"#5689B3"});
              }
              else
              {
                  driveFull.attr({fill:"#F03F03"});
              }
             var text = fslm.paper.text(x+(fslm.drives.drawWidth*0.5),y+(fslm.drives.drawHeight/2),drve.name + " ("+Math.round(percentage* 100)+"%)");
             text.attr({cursor:"pointer","font-size":16});
             text.click(function() { document.location= drve.link });
             var fname = "";
             if (drve.type == "M")
             {
                 fname = "/static/images/up.gif";
             }
             else
             {
                 fname = "/static/images/down.gif";
             }
             var text2 = fslm.paper.image(fname, x+(fslm.drives.drawWidth*0.1), y+(fslm.drives.drawHeight*0.3), 20,20);
             text2.attr({"font-size":20});
             
    },
    drawXPadding: 10,
    drawYPadding: 10,
	drawHeight: 40,
	drawWidth: 300,
    drawFontSize:18,
	drawColour:'#efefef'
},
paper : {},
initRaphael : function(callback) {
	fslm.paper = Raphael("drives",0,0,80,800);
    if (callback)
        callback();
},
init : function() {
		fslm.drives.getDrivesSize(function() {
            fslm.initRaphael(function() {
                fslm.drives.drawDrives()
                $('svg').attr('height','500')
            })
        });
}

}
$(document).ready(function() { 

fslm.init();
});

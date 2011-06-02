fslm = {
drives : {
	sizeData : {},
	getDrivesSize: function(){
	  $.get('/driveslist',function(data) {
		eval('fslm.drives.sizeData = ' + data)
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
			 var drive = fslm.paper.rect(x,y,fslm.drives.drawWidth,fslm.drives.drawHeight);
             drive.click(function() { document.location= drve.link });
			 drive.attr({stroke:"#000","stroke-width":"0.2",fill: "#DEDEDE","font-size":fslm.drives.drawFontSize});
             var percentage = (drve.used/ drve.capacity) ;
             var driveFull = fslm.paper.rect(x,y,fslm.drives.drawWidth*percentage,fslm.drives.drawHeight);
             driveFull.click(function() { document.location= drve.link });
             if (drve.isOver == "False")
             {
                driveFull.attr({fill:"#5689B3"});
              }
              else
              {
                  driveFull.attr({fill:"#D92B2B"});
              }
             var text = fslm.paper.text(x+(fslm.drives.drawWidth*0.5),y+(fslm.drives.drawHeight/2),drve.name + " ("+Math.round(percentage* 100)+"%)");
	      text.click(function() { document.location= drve.link });
             
    },
    drawXPadding: 10,
    drawYPadding: 10,
	drawHeight: 40,
	drawWidth: 100,
    drawFontSize:12,
	drawColour:'#efefef'
},
paper : {},
initRaphael : function() {
	fslm.paper = Raphael("drives",0,0,80,800);
},
init : function() {
	fslm.drives.getDrivesSize();
	fslm.initRaphael()
    setTimeout('fslm.drives.drawDrives()',600);
}

}
$(document).ready(function() { 
fslm.init();
});

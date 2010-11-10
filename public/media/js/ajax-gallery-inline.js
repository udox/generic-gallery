/*
Ajax call that takes div id name from images which corosponds to the actual image id
of the photo object in db.
Using this we used the GalleryPhoto model to create if necessary the correct size
image thumbnail

Dependencies: 
id and class names!
jquery lib
json2 lib (json parsing from django)
ajax view

*/

$(document).ready(function(){
    $(".grid-inline img").click(function(){
        sendValue($(this).attr("id"));
    });
	// we call sendValue function at start so we can have the first image in gallery
	// appear on page load 
	sendValue($(".grid-inline img:first").attr("id"));        
});

function sendValue(id){
    $.post("/gallery/inline/inline-callback/", {                
        img: id,
		type: 'json'                    
     },
    function(data){
		$('#ajax-inline').html(data);
    }, "html");
};
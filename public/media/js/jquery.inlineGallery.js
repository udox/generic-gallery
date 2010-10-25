/* Handles moving through a gallery of images inline on a page and not using a
 * lightbox. In admin choose "main layout" for the render size in the admin
 * for it to use the inline-gallery.html template.
*         ~jaymz
 */

;(function($) {
    $.fn.inlineGallery = function() {
        return this.each(function() {
            $(this).children('.gallery-image').hide();
            $(this).children('.gallery-image:first').show();

            var imgs = Array();
            $(this).children('.gallery-image').each(function() {
                imgs.push($(this).attr('id'));
            });
            var current = 0; // the index that is currently being shown
            var prev = current;
            var max = imgs.length-1;

            function updateImages() {
                $('#'+imgs[current]).show().addClass('gallery-image-active');
                $('#'+imgs[prev]).show().removeClass('gallery-image-active');
            }

            $(this).children('.gallery-controls').children('.gallery-previous').bind('click', function() {
                prev = current;
                if(current-1<0) {
                    current = max;
                } else {
                    current -= 1;
                }
                updateImages();
            });
            $(this).children('.gallery-controls').children('.gallery-next').bind('click', function() {
                prev = current;
                if(current+1>max) {
                    current = 0;
                } else {
                    current += 1;
                }
                updateImages();
            });
        });
    };
})(jQuery);


function preview_src(src)
{
    if (src.match(/(p[a-z]\.)jpg/)) {
        return src.replace(RegExp.$1, 'pl.');
    } else if (src.match(/consumer_game/)) {
        return src.replace('js-','-');
    } else if (src.match(/js\-([0-9]+)\.jpg$/)) {
        return src.replace('js-','jp-');
    } else if (src.match(/ts\-([0-9]+)\.jpg$/)) {
        return src.replace('ts-','tl-');
    } else if (src.match(/(\-[0-9]+\.)jpg$/)) {
        return src.replace(RegExp.$1, 'jp' + RegExp.$1);
    } else {
        return src.replace('-','jp-');
    }
}


$(document).ready(function() {

    $(".img_s").click(function(){
        var img_s = $(this).attr('src');
        var img_l = preview_src(img_s);
        $(this).attr('src',img_l);

        $(this).click(function(){
            $(this).attr('src',img_s)

        });

    });

});
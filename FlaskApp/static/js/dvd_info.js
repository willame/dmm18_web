 var sample_img_cursor = "";
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
     function find_current_img_block(sample_img_cursor){
        var re=/-(\d+\.[jpgn]+)$/;
        match = re.exec(sample_img_cursor);
        return $('div.sample-img-element img[src*="'+match[0]+'"]').parent().parent();


    }

        // Get the modal
    var modal = document.getElementById('myModal');

    // Get the <span> element that closes the modal
    var span = document.getElementById('close-display');


    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
        document.getElementById('display').innerHTML="";
        modal.style.display = "none";
         $('#sample-img-control').css('display','none');


    }



    $('span#prev-btn').click(
            function(){
                    var current_img_block = find_current_img_block(sample_img_cursor);
                    var prev_img_block = current_img_block.prev();
                    if(prev_img_block.length>0) {
                        $('#next-btn').html("");
                        console.log("current:"+sample_img_cursor);
                        sample_img_cursor = prev_img_block.find('img[src]').attr('src');
                        console.log("next:"+sample_img_cursor);
                        $("#display img").attr('src',preview_src(sample_img_cursor));
//                        sample_img_cursor = prev_img_src_s;

            }else{
                 $('#next-btn').html("到底了");
                 }

            }
           );

           $('span#next-btn').click(
            function(){
                    var current_img_block = find_current_img_block(sample_img_cursor);
                  var next_img_block =  current_img_block.next();
//                var current_img_block = find_current_img_block(sample_img_cursor);
//                 = current_img_block;
                if(next_img_block.length>0) {
                $('#next-btn').html("");
                    console.log("current:"+sample_img_cursor);
                    sample_img_cursor = next_img_block.find('img[src]').attr('src');
                    console.log("next:"+sample_img_cursor);
                    $("#display img").attr('src',preview_src(sample_img_cursor));
//                    sample_img_cursor = next_img_src_s;
                 }else{
                 $('#next-btn').html("到底了");
                 }
            }
           );

//-----------------------------------------------
    $(".img_s").click(function(){
        var img_s = $(this).attr('src');

        var img_l = preview_src(img_s);
        //$(this).attr('src',img_l);
//        location.hash = "#" + "popup1";
console.log("current:"+sample_img_cursor);

        sample_img_cursor = img_s;

        console.log("next:"+sample_img_cursor);
//        var re=/-(\d+\.[jpgn]+)$/;
//        match = re.exec(img_s);
//        var current_img_block = $('div.sample-img-element img[src*="'+match[1]+'"]').parent().parent();
//        var prev_img_block = current_img_block.prev();
//        var next_img_block = current_img_block.next();

//        control = ''+prev_btn+next_btn+''
//        $('#img-control').html(control);



        modal.style.display = "block";
        $('#sample-img-control').css('display','block');
        $("#display").html("<img height='100%'class='img-responsive' alt='sample_l' src='"+img_l+"'>")
//         document.getElementById("display-title").innerHTML+=" 样图";
//        $(this).click(function(){
//            $(this).attr('src',img_s)
//
//        });
//        if(prev_img_block.length>0) {
//            var prev_img_src_s = prev_img_block.find('img[src]').attr('src');
//           $('span#prev-btn').click(
//            function(){
//
//                 $("#display img").attr('src',preview_src(prev_img_src_s));
//                 sample_img_cursor = prev_img_src_s;
//            }
//           );
//            }


//        if(next_img_block.length>0) {
//            var next_img_src_s = next_img_block.find('img[src]').attr('src');
//
//            $('span#next-btn').click(
//            function(){
//                 $("#display img").attr('src',preview_src(next_img_src_s));
//                 sample_img_cursor = next_img_src_s;
//            }
//           );
//        }

    });

    $(".sample_video").click(function(){
        modal.style.display = "block";
        var src = $(this).attr('href');
        $("#display").html("<video width='100%' autoplay controls><source src='"+
        src
        +"'  type='video/mp4'></video>");
//        document.getElementById("display-title").innerHTML+=" 样片";
    });





});
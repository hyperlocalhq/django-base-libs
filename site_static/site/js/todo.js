    <script>
    $(window).load(function(){
        $("#next").click(function() {
            var $next, $selected = $(".current");
            $selected.removeClass("current").removeClass("todo").addClass("done");
            $next = $selected.next().removeClass("todo").addClass("current");
            if (!$next.length) {
                $(".done").removeClass("done").addClass("todo");
            }
        });
        
        $("#prev").click(function() {
            var $prev, $selected = $(".current");
            $selected.removeClass("current").removeClass("done").addClass("todo");
            $prev = $selected.prev().removeClass("done").addClass("current");
            if (!$prev.length) {
                $(".done").removeClass("done").addClass("todo");
            }
        });
    });
    </script>
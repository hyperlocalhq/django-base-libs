
var django = {
  jQuery: jQuery
};

$(function() {
  $("a[href^='http://']").attr("target","_blank");

    if ($('#cms_toolbar').length) { // cms toolbar fix
      if ($('body').css('margin-top') == "-43px") {
        $('body').css('margin-top', 0);
      }
    }
  });
$(function() {
  $('#to-top').click(function(e){
    $('html, body').animate({scrollTop:0}, 'slow');
    return false;
  });

  $(window).scroll(function() {
    if ($('body').offset().top < $(window).scrollTop()) {
      $('#to-top').addClass('on');
    } else {
      $('#to-top').removeClass('on');
    }
  });

  $('.grid .item .cancel').click(function(){
    $('#item-preview').attr("id","")
  });

  $('.grid .item > a').click(function(){
    if($(this).parents('.item').attr("id")) {
      $('#item-preview').attr("id","");
    } else {
      $('#item-preview').attr("id","");
      $(this).parents('.item').attr("id","item-preview");
    }

    item = $(this).parents('.item')
    var left = item.position().left;
    var width = ($("#container").width());

    // var test = item.css('-webkit-transform').match(/matrix(?:(3d)\(-{0,1}\d+(?:, -{0,1}\d+)*(?:, (-{0,1}\d+))(?:, (-{0,1}\d+))(?:, (-{0,1}\d+)), -{0,1}\d+\)|\(-{0,1}\d+(?:, -{0,1}\d+)*(?:, (-{0,1}\d+))(?:, (-{0,1}\d+))\))/)
    // console.log(test)
    // console.log(left, width);

    item.find(".description").css({left: -left, width: width});

    $('#container').isotope();
    return false
  });
});

window.onresize = function(event) {
  $('#container').isotope({
    onLayout: function() {
      item = $('#item-preview')
      var left = item.position().left;
      var width = $("#container").width();
      item.find(".description").css({left: -left, width: width});
    }
  });
}

$(document).ready(function(){
// $(window).load(function() {
  var $container = $('#container'),
  filters = {};

  $container.isotope({
    itemSelector : '.item',
    layoutMode : 'fitRows'
  });

  // filter buttons
  $('.filter a').click(function(e){
    e.preventDefault();
    var $this = $(this);
    var $li = $this.closest('li');

    var $optionSet = $this.closest('.option-set');
    // store filter value in object
    // i.e. filters.category = ['.cat_history']
    var group = $optionSet.attr('data-filter-group');
    filters[group] = filters[group] || [];
    var value = $this.attr('data-filter-value');
    var single_selection = $optionSet.attr('data-single-selection');
    var hierarchical = $optionSet.attr('data-hierarchical');
    var level = parseInt($li.attr('data-level'), 10);
    var children_selector = $this.attr('data-level-1-at');
    var target_child = $this.attr('data-target');
    var $children;
    if (children_selector) {
      $children = $(children_selector);
    } else if (level == 1) {
      $children = $this.closest('.level-1-container');
    }

    if (value) {
      if ($this.hasClass('selected')) {
        $this.removeClass('selected');
        $li.removeClass('selected');
        if ($children && level == 0) {
          $children.find('a.selected').click();
          $children.find('ul.in').removeClass('in');
        }
        filters[group] = jQuery.grep(filters[group], function(v) {
          return v != value;
        });
            // remove the corresponding item from filter summary
            $('#filter_summary li[data-filter-group="' + group + '"][data-filter-value="' + value + '"]').remove();
            if ($('#filter_summary').children().length == 1) {
              $('#filter_summary').empty();
            }
          } else {
            if (hierarchical) {
              if (single_selection) {
                // unselect previously selected
                // and collect filters
                if (level == 0) {
                  $optionSet.find('a.selected').click();
                  if ($children) {
                    $children.find('ul.in').removeClass('in');
                  }
                  filters[group] = [value];
                } else {
                  if ($children) {
                    $children.find('a.selected').click();
                  }
                  filters[group].push(value);
                }
              } else {
                filters[group].push(value);
              }
            } else {
              if (single_selection) {
                // unselect previously selected
                // and collect filters
                $optionSet.find('a.selected').click();
                filters[group] = [value];
              } else {
                filters[group].push(value);
              }
            }
        // change selected class
        $this.addClass('selected');
        $li.addClass('selected');
        if ($children) {
          $children.find(target_child).addClass('in');
        }
        if ($('#filter_summary').text() == "") {
          var $li = $('<li><b>' + str_filter_selection + ':</b></li>');
          $('#filter_summary').append($li);
        }
        var $li = $('<li data-filter-group="' + group + '" data-filter-value="' + value + '"><a href="">' + $this.text() + '</a></li>');
        $('#filter_summary').append($li);
      }
    }

  // convert object into array
  var isoFilters = [];
  for (var prop in filters) {
  isoFilters.push(filters[prop].join(''));
  }
  var selector = isoFilters.join('');

  $.bbq.pushState({filter: selector});

  $container.isotope({filter: selector});
  $(".img img:in-viewport").lazyload();
  $container.trigger("map_filter", { filter: isoFilters});
  $(".isotope-item:not(.isotope-hidden) .img", $container).trigger("appear");

  return false;

});

$('#filter_summary a').live('click', function(e) {
  e.preventDefault();
  var $this = $(this).closest('li');
  var group = $this.attr('data-filter-group');
  var value = $this.attr('data-filter-value');
  if (!group && !value) {
    // trigger the clicks on all selected filters
    $('#filters a.selected').click();
  } else {
    // trigger the click on corresponding filter
    $('.filter[data-filter-group="' + group + '"] a[data-filter-value="' + value + '"]').click();
  }
})

$('#filter_reset').live('click', function(e) {
  e.preventDefault();
  $('#filters a.selected').click();
})

if (window.location.hash) {
    // get options object from hash
    var options = window.location.hash ? $.deparam.fragment(window.location.hash, true) : {};
    // apply options from hash
    $(options.filter.split('.')).each(function() {
      if (!this) {
        return;
      }
      $('#filters a[data-filter-value=".' + this + '"]').click();
    })
  }
});

$(document).ready(function(){
  $(".img img").lazyload();
});

$(window).bind('scrollstop', function(e){
  $(".img img:in-viewport").lazyload().addClass("in");
});

$(window).load(function() {
  if ($("[data-toggle=tooltip]").length) {
    $("[data-toggle=tooltip]").tooltip({
      container: '.container'
    });
  }

   $('.panel-collapse').collapse('show');
});

$(function() {
  $("a[href^='http://']").attr("target","_blank");

  if ($('#cms_toolbar').length) { // cms toolbar fix
    $('body').addClass('cms-toolbar-visible')
  }
});

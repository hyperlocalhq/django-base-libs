function init_share(){
  $('.share-twitter').sharrre({
    share: {
      twitter: true
    },
    template: '<span class="icon icon-social-twitter"></span> <span class="sr-only">{% trans "Share on Twitter" %}</span>',
    enableHover: false,
    enableTracking: true,
    buttons: { twitter: {via: 'BERLINBUEHNEN'}},
    click: function(api, options){
      api.simulateClick();
      api.openPopup('twitter');
    }
  });

  $('.share-facebook').sharrre({
    share: {
      facebook: true
    },
    template: '<span class="icon icon-social-facebook"></span> <span class="sr-only">{% trans "Share on Facebook" %}</span>',
    enableHover: false,
    enableTracking: true,
    click: function(api, options){
      api.simulateClick();
      api.openPopup('facebook');
    }
  });
}

$(document).ready(init_share);
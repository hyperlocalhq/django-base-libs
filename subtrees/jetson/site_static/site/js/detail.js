
$('.share-twitter').sharrre({
  share: {
    twitter: true
  },
  template: 'Share on Twitter',
  enableHover: false,
  enableTracking: true,
  buttons: { twitter: {via: 'MUSEUMSPORTAL'}},
  click: function(api, options){
    api.simulateClick();
    api.openPopup('twitter');
  }
});

$('.share-facebook').sharrre({
  share: {
    facebook: true
  },
  template: 'Share on Facebook',
  enableHover: false,
  enableTracking: true,
  click: function(api, options){
    api.simulateClick();
    api.openPopup('facebook');
  }
});

$('.share-image-twitter').sharrre({
  share: {
    twitter: true
  },
  template: '<span class="icon icon-social-twitter"></span> <span class="sr-only">{% trans "Share on Twitter" %}</span>',
  enableHover: false,
  enableTracking: true,
  buttons: { twitter: {via: 'MUSEUMSPORTAL'}},
  click: function(api, options){
    api.simulateClick();
    api.openPopup('twitter');
  }
});

$('.share-image-facebook').sharrre({
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

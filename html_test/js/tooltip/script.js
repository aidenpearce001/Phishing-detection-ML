/**
 * Created by 1 on 10.10.2015.
 */

$(document).ready(function() {

  $('.js-mytooltip').myTooltip();

  $('.js-mytooltip-content').myTooltip({
    'offset': 15,
    'theme': 'light',
    'customClass': 'mytooltip-content',
    'cursorHelp': true,
    'content':
    '<p><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Mars_23_aug_2003_hubble.jpg/1024px-Mars_23_aug_2003_hubble.jpg">' +
    'Mars is the fourth planet from the Sun and the second smallest planet in the Solar System, after Mercury.' +
    '  Named after the Roman god of war, it is often referred to as the "Red Planet" because the iron oxide prevalent' +
    ' on its surface gives it a reddish appearance. <br> ' +
    '<a href="https://en.wikipedia.org/wiki/Mars" target="_blank">read more</a><p>'
  });


  $('.js-p-title').find('a').myTooltip({
    'fromTitle': true
  });

  // custom-events
  $('.custom-event').on('show-before', function(event) {
    console.log('show-before!')
  });

  $('.custom-event').on('show-complete', function(event, content) {
    console.info(content);
    console.log('show-complete!');
  });

  $('.custom-event').on('hide-before', function(event) {
    console.log('hide-before!');
  });

  $('.custom-event').on('hide-complete', function(event) {
    console.log('hide-complete!');
  });

  // destroy
  $('.destroy-element').on('click', function(event) {
    event.preventDefault();
    $('.destroy-current').myTooltip('destroy');
  });

  // call
  setTimeout(function() {
    $('.download-header').myTooltip('call');
  }, 300);

  $('.add-element').on('click', function(event) {
    event.preventDefault();
    $(this).after('<br><div style="margin: 10px 0;" class="js-mytooltip type-inline-block style-block style-block-three"' +
        ' data-mytooltip-animate-duration="150" data-mytooltip-direction="left" data-mytooltip-custom-class="align-center"' +
        ' data-mytooltip-content="Wow!<br> This dinamic element!">New element</div>');

    $('.js-mytooltip').myTooltip('update');

  });

  // dinamic template
  $(document).on('click', '.add-to-basket', function(event) {
    event.preventDefault();

    // template
    var countElement = $(this).next('.count');
    var countNumber = countElement.text();
    countElement.text(++countNumber);

    // tooltip
    var tooltip = $('.js-mytooltip[data-mytooltip-id="' + $(this).parents('div').last().data('mytooltip-id') + '"]');
    tooltip.myTooltip('updateContent', $(this).closest('.wrap').clone().wrap('<div>').parent().html());

  });


});

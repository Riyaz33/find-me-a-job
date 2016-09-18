(function() {
  var $tiles = document.querySelectorAll('.tile');

  if (!$tiles) {
    return;
  }

  [].slice.call($tiles).forEach(function(el) {
    el.addEventListener('click', function() {
      openInNewTab('http://stackshare.io/search/q=' + el.querySelector('.name').innerHTML)
    });
  });
})()

function openInNewTab(url) {
  var win = window.open(url, '_blank');
  win.focus();
}

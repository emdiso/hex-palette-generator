import ColorThief from './node_modules/colorthief/dist/color-thief.mjs'

const colorThief = new ColorThief();

window.addEventListener('load', function() {
  $('#save').hide();
  $('#create-box').hide();
  document.querySelector('input[type="file"]').addEventListener('change', function() {
    if (this.files && this.files[0]) {
      $('#create-box').show();

      var img = document.querySelector('#myImg');
      img.onload = () => {

        if (img.complete) {
          var colors = colorThief.getPalette(img,6);

          for(let i=1; i<7; i++){
            var paletteColor = $('#c'+i);
            var boxColor = $('#h'+i);
            var hex = rgbToHex(colors[i-1][0], colors[i-1][1], colors[i-1][2]);

            paletteColor.css('background-color', hex);
            boxColor.css('background-color', hex);
            $("p#hex"+i).text(hex);
            $("#color"+i).attr('value', hex);
          }

          var dominant = rgbToHex(colors[0][0], colors[0][1], colors[0][2]);
          $('#banner').css('background-color', dominant);
        }
			}

      img.src = URL.createObjectURL(this.files[0]);
      $("#smallVersion").attr('src', img.src);
      $("#form-image").attr('value', img.src);
      $('#save').show();
    }
  });
});

// also taken from color thief -- converts RGB value to HEX
const rgbToHex = (r, g, b) => '#' + [r, g, b].map(x => {
  const hex = x.toString(16)
  return hex.length === 1 ? '0' + hex : hex
}).join('')

// WHEN SAVE IS CLICKED
$('.popupButton').click(function() {
  $('#create-box').hide();
  $('#upload').hide();
  $('#banner').hide();
  $('.content').toggle();
});

$('#cancel').click(function() {
  $('.content').toggle();
  $('#create-box').show();
  $('#upload').show();
  $('#banner').show();
});

var $grid = $('.grid').isotope({
  itemSelector: '.product',
  layoutMode: 'fitRows',
  getSortData: {
    nombre: function( itemElem ) {
      // get text of .weight element
      var nombre = $( itemElem ).find('.nombre').text();
      // replace parens (), and parse as float
      return nombre;
    },
    precio: function( itemElem ) { // function
        var precio = $( itemElem ).attr("precio");
        return parseInt(precio);
    },
    id: function( itemElem ) { // function
        var id = $( itemElem ).attr("IDD");
        return parseInt(id);
    }
  }
});

var type = []
var major = []

$('#type input[type=checkbox]').on('click',function(){
  type = []
  $('input[name=typeOp]:checked').map(function(i,t){ type.push($(t).val())});
  console.log(concatFilters())
  $grid.isotope({ filter: concatFilters()});
});

$('#major input[type=checkbox]').on('click',function(){
  major = []
  $('input[name=typeMajor]:checked').map(function(i,t){ major.push($(t).val())});
  console.log(concatFilters( ))
  $grid.isotope({ filter: concatFilters( ) });
});

function concatFilters() {
  let value = '';
  if( type.length != 0 && major.length !=0){
    for ( let t in type ) {
      for (let m in major ){
        value += ',.'+type[t]+'.'+major[m];
      }
    }
  } else if (type.length == 0) {
      for (let m in major ){
        value += ',.'+major[m];
      }
  } else {
    for ( let t in type ) {
      value += ',.'+type[t];
    }
  }
  return value.slice(1);
};

$('.filters').on( 'click', '.b ', function() {
  var $this = $(this);
  // get group key
  var $buttonGroup = $this.parents('.button-group');
  var filterGroup = $buttonGroup.attr('data-filter-group');
  // set filter for group
  filters[ filterGroup ] = $this.attr('data-filter');
  // combine filters
  var filterValue = concatValues( filters );
  // set filter for Isotope
  $grid.isotope({ filter: filterValue });
});

// bind sort button click
$('#sorts').on( 'click', 'button', function() {
  var sortByValue = $(this).attr('data-sort-by');
  $grid.isotope({ sortBy: sortByValue });
});

// change is-checked class on buttons
$('.button-group').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $buttonGroup.on( 'click', 'button', function() {
    $buttonGroup.find('.is-checked').removeClass('is-checked');
    $( this ).addClass('is-checked');
  });
});

function concatValues( obj ) {
  var value = '';
  for ( var prop in obj ) {
    value += obj[ prop ];
  }
  return value;
};


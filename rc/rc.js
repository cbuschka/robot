const actions = ['m1f', 'm1b', 'lm1f','lm1b','lm2f','lm2b', 'say' ];
  forEachButton((button) => {
    button.addEventListener('mousedown', handlePressed);
    button.addEventListener('touchstart', handlePressed);
    button.addEventListener('mouseleave', handleUnpressed);
    button.addEventListener('mouseup', handleUnpressed);
    button.addEventListener('touchend', handleUnpressed);
  });

function handlePressed(ev) {
  ev.target.classList.add('pressed');
}

function handleUnpressed(ev) {
  ev.target.classList.remove('pressed');
}

function forEachButton(f) {
  const elementList = document.getElementsByTagName("button");
  for(let i=0; i<elementList.length; ++i) {
    f(elementList[i], i);
  }
}

let lastQueryParams = 'action=stop';

function pollButtons() {
  const selectedActions = [];
  forEachButton((button) => {
   actions.forEach((action) => {
    if( button.classList.contains("pressed") && button.classList.contains(action) && selectedActions.indexOf(action) === -1 ) {
      selectedActions.push(action);
    }
   });
  });

  if( selectedActions.length === 0 ) {
    selectedActions.push("stop");
  }

  const loc = window.location;
  const queryParams = selectedActions.map((action) => "action="+action).join("&");
  if( lastQueryParams !== queryParams ) {
    console.log('sending %o', queryParams);
    fetch(loc.protocol+'//'+loc.host+'/api/rc?'+queryParams, {method:'POST'})
      .catch((e) => { console.error(e); } );
    lastQueryParams = queryParams
  }
}

window.setInterval(pollButtons, 100);

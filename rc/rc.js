const actions = ['forward','backward','left','right', 'say', 'motor1' ];
const buttons = {};
actions.forEach((name) => {
  const element = document.getElementById(name);
  element.addEventListener('mousedown', (ev) => { handleEvent(ev, name); } );
  element.addEventListener('touchstart', (ev) => { handleEvent(ev, name); } );
  element.addEventListener('mouseleave', (ev) => { handleEvent(ev, "stop"); } );
  element.addEventListener('mouseup', (ev) => { handleEvent(ev, "stop"); } );
  element.addEventListener('touchend', (ev) => { handleEvent(ev, "stop"); } );
  buttons[name] = element;
});

let action = 'stop';

function handleEvent(ev, newAction) {
  action=newAction;
  ev.preventDefault();
  ev.stopPropagation();
  updateUi();
}

function updateUi() {
 actions.forEach((name) => {
   let element = buttons[name];
   if( action === name ) {
     element.classList.add("pressed");
   } else {
     element.classList.remove("pressed");
   }
 });
}

let lastAction='stop';
function pollButtons() {
  for(let key in buttons) {
    if( buttons[key].pressed ) {
      if( action !== 'stop' ) {
        console.log('multiple actions: %o and %o. aborting.',action,key);
        return;
      }
      action = key;
    }
  }

  if( lastAction !== action ) {
  console.log("action: "+action);
  const loc = window.location;
  fetch(loc.protocol+'//'+loc.host+'/api/rc?action='+action, {method:'POST'}).catch((e) => { console.error(e); } );
  lastAction = action;
  }
};

window.setInterval(pollButtons, 100);

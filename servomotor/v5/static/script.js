document.addEventListener('DOMContentLoaded', function () {
  const joystick = document.getElementById('joystick');
  const handle = document.getElementById('joystick-handle');
  const axisXElement = document.getElementById('axis-x');
  const axisYElement = document.getElementById('axis-y');
  const savedCoordinatesElement = document.getElementById('saved-coordinates');

  const joystickRadius = joystick.clientWidth / 2;
  let isDragging = false;
  let lastPosition = { x: 0, y: 0 };

  joystick.addEventListener('mousedown', startDragging);
  document.addEventListener('mousemove', handleDragging);
  document.addEventListener('mouseup', stopDragging);

  function startDragging(e) {
    isDragging = true;
    handle.style.transition = 'transform 0.1s ease-out';
    handleDragging(e);
  }

  function stopDragging() {
    isDragging = false;
    resetHandle();
  }

  function handleDragging(e) {
    const rect = joystick.getBoundingClientRect();
    const centerX = rect.left + joystickRadius;
    const centerY = rect.top + joystickRadius;
    let deltaX = e.clientX - centerX;
    let deltaY = e.clientY - centerY;

    const distance = Math.sqrt(deltaX ** 2 + deltaY ** 2);
    if (distance > joystickRadius) {
      const angle = Math.atan2(deltaY, deltaX);
      deltaX = joystickRadius * Math.cos(angle);
      deltaY = joystickRadius * Math.sin(angle);
    }

    const posX = deltaX / joystickRadius;
    const posY = deltaY / joystickRadius;

    handle.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    updateAxisValues(posX, posY);

    // Mappa l'intervallo -1 a 1 nel range 0 a 180
    const mappedX = map(posX, -1, 1, 0, 180);
    const mappedY = map(posY, -1, 1, 0, 180);

    if (isDragging) {
      // Invia le coordinate al server Flask solo se il joystick è in movimento
      sendCoordinates(mappedX, mappedY);
    }
  }

  function resetHandle() {
    handle.style.transition = 'transform 0.3s ease-out';
    handle.style.transform = 'translate(0, 0)';
    updateAxisValues(lastPosition.x, lastPosition.y);
    sendCoordinates(lastPosition.x, lastPosition.y);
  }

  function updateAxisValues(x, y) {
    axisXElement.textContent = `X: ${Math.round(x * 180)}`;
    axisYElement.textContent = `Y: ${Math.round(y * 180)}`;
    savedCoordinatesElement.textContent = `Saved: ${Math.round(lastPosition.x * 180)}, ${Math.round(lastPosition.y * 180)}`;
  }

  function sendCoordinates(x, y) {
    // Memorizza l'ultima posizione del joystick
    lastPosition = { x, y };

    // Invia le coordinate al server Flask tramite una richiesta AJAX
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/control', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.send(`angle_x=${Math.round(x)}&angle_y=${Math.round(y)}`);
  }

  // Funzione di mappatura per convertire un valore da un intervallo all'altro
  function map(value, in_min, in_max, out_min, out_max) {
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
  }
});

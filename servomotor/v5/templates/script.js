document.addEventListener('DOMContentLoaded', function () {
  const joystick = document.getElementById('joystick');
  const handle = document.getElementById('joystick-handle');
  const axisXElement = document.getElementById('axis-x');
  const axisYElement = document.getElementById('axis-y');

  const joystickRadius = joystick.clientWidth / 2;
  let isDragging = false;
  let lastPosition = { x: 0, y: 0 };

  joystick.addEventListener('mousedown', startDragging);
  document.addEventListener('mousemove', handleDragging);
  document.addEventListener('mouseup', stopDragging);

  function startDragging(e) {
    isDragging = true;
    handle.style.transition = 'none';
    handleDragging(e);
  }

  function stopDragging() {
    isDragging = false;
    handle.style.transition = '0.3s ease-out';
    resetHandle();
  }

  function handleDragging(e) {
    if (isDragging) {
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
      lastPosition = { x: posX, y: posY };
      updateAxisValues(posX, posY);
      sendJoystickCoordinates(posX, posY);
    }
  }

  function resetHandle() {
    handle.style.transform = 'translate(0, 0)';
    updateAxisValues(lastPosition.x, lastPosition.y);
    sendJoystickCoordinates(lastPosition.x, lastPosition.y);
  }

  function updateAxisValues(x, y) {
    axisXElement.textContent = `X: ${Math.round(x * 180)}`;
    axisYElement.textContent = `Y: ${Math.round(y * 180)}`;
  }

  function sendJoystickCoordinates(x, y) {
    fetch('/control', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ angle_x: Math.round(x * 180), angle_y: Math.round(y * 180) }),
    });
  }
});

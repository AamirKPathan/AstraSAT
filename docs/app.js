const form = document.querySelector('#flight-form');
const fields = ['mass', 'altitude', 'safe-speed', 'time', 'velocity', 'wind', 'direction'];
const value = (id) => Number(document.querySelector(`#${id}`).value) || 0;

function bearingName(degrees) {
  const names = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  return names[Math.round(degrees / 45) % 8];
}

function calculate() {
  const altitude = value('altitude');
  const velocity = value('velocity');
  const wind = value('wind');
  const direction = value('direction');
  const safeSpeed = value('safe-speed');
  const descentSpeed = Math.abs(velocity);
  const descentTime = descentSpeed > 0 ? altitude / descentSpeed : 0;
  const drift = wind * descentTime;
  const isSafe = velocity < 0 && descentSpeed <= safeSpeed;

  document.querySelector('#landing-state').textContent = isSafe ? 'SAFE LANDING' : 'REVIEW LANDING';
  document.querySelector('#state-detail').textContent = isSafe
    ? 'Within configured descent limits.'
    : velocity >= 0 ? 'Descent is not yet detected.' : 'Descent speed exceeds your configured limit.';
  document.querySelector('#descent-time').textContent = `${descentTime.toFixed(1)} s`;
  document.querySelector('#wind-drift').textContent = `${drift.toFixed(1)} m`;
  document.querySelector('#bearing').textContent = `${bearingName(direction)} · ${direction.toFixed(0)}°`;
  document.querySelector('#profile-caption').textContent = `${altitude.toFixed(0)} m / ${value('time').toFixed(0)} s`;
  document.querySelector('.axis-y').textContent = `${altitude.toFixed(0)} m`;
  document.querySelector('.axis-x').innerHTML = `0 s <b>·</b> ${value('time').toFixed(0)} s`;
}

form.addEventListener('submit', (event) => {
  event.preventDefault();
  calculate();
});

fields.forEach((id) => document.querySelector(`#${id}`).addEventListener('input', calculate));
calculate();

document.addEventListener("DOMContentLoaded", function () {
  const now = new Date();
  const currentHour = now.getHours();

  const majorHours = [0, 6, 9, 12, 15, 18];
  let activeBlockStartHour = 0;

  for (const hour of majorHours) {
    if (currentHour >= hour) {
      activeBlockStartHour = hour;
    } else {
      break;
    }
  }

  const currentDayColumn = document.querySelector(".day-column.current-day");
  let activeBlockElement = null;

  if (currentDayColumn) {
    activeBlockElement = currentDayColumn.querySelector(
      `.time-slot[data-time="${activeBlockStartHour}"]`
    );
    if (activeBlockElement) {
      activeBlockElement.classList.add("current-time-block");
    }
  }
});

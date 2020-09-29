const nameInput = document.getElementById('name');
const valueInput = document.getElementById('value');
const expenseForm = document.getElementById('expense-form');

if (nameInput && valueInput && expenseForm) {
	expenseForm.addEventListener('submit', (e) => {
		let isNameValid = true;
		let isValueValid = true;

		const name = valueInput.value;
		if (!name || !name.trim() || name.length > 25) {
			isNameValid = false;
		}

		const value = Number(valueInput.value);
		if (!value || value > 9999) {
			isValueValid = false;
		}

		if (!isValueValid || !isNameValid) {
			e.preventDefault();
		}
	})

	nameInput.focus();
}

const newMonthForm = document.getElementById('new-month-form');
const newMonthNameInput = document.getElementById('month_name');

if (newMonthNameInput && newMonthForm) {
	newMonthForm.addEventListener('submit', (e) => {
		if (!newMonthNameInput.value || !newMonthNameInput.value.trim()) {
			e.preventDefault();
		}
	})
}

const monthSelect = document.getElementById('month-select');

if (monthSelect) {
	monthSelect.addEventListener('change', (e) => {
		window.location.replace(`${window.location.origin}/${e.target.value}`);
	});
}

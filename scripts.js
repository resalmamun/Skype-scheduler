document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    // Collect form data
    const message = document.getElementById('message').value;
    const datetime = document.getElementById('datetime').value;
    const receivers = document.getElementById('receivers').value.split(',');
    const weekly = document.getElementById('weekly').checked;

    // Send the data to the backend using fetch API
    fetch('/schedule_message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: message, datetime: datetime, receivers: receivers, weekly: weekly })
    })
    .then(response => response.json())
    .then(data => {
        // Display the new task in the list
        const taskList = document.getElementById('taskList');
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <div>
                <strong>Message:</strong> "${message}"
                <br>
                <strong>Scheduled for:</strong> ${datetime}
                <br>
                <strong>Receivers:</strong> ${receivers.join(', ')}
            </div>
            <span>Scheduled</span>
        `;
        taskList.appendChild(listItem);

        // Show confirmation message
        const confirmationMessage = document.getElementById('confirmationMessage');
        confirmationMessage.style.display = 'block';

        // Clear the form
        document.getElementById('message').value = '';
        document.getElementById('datetime').value = '';
        document.getElementById('receivers').value = '';
        document.getElementById('weekly').checked = false;
    })
    .catch(error => {
        console.error('Error scheduling message:', error);
    });
});

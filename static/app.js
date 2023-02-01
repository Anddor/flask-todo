function getStarIcon(isFav) {
    if (isFav) {
        return "bi-star-fill"
    } else {
        return "bi-star"
    }
}


function deleteTask(taskId) {
    const taskElement = document.querySelectorAll(`[data-task-id="${taskId}"]`)[0];

    // Update Model
    fetch(`../api/todos/${taskId}`,
    {
        method: "DELETE"
    }).then(
        response => {
            if (response.status == 204) {
                // Delete success, update view:
                taskElement.remove();
            }
        }
    )

}

function update(taskId, task, fav) {
    // Update Model
    fetch(`../api/todos/${taskId}`,
    {
        method: "PUT",
        headers: new Headers({"Content-Type": "application/json"}),
        body: JSON.stringify({
            task: task,
            fav: fav
        })
    }).then(
        response => {
            if (response.status == 200) {
                // Update success, update View:
                refreshTaskList(); // YOLO    
            }
        }
    )
}


function updateViewWithListItem(modelElement) {
    const list = document.getElementById('task-list');
    updateViewWithListItem(list, modelElement);
}

function updateViewWithListItem(view, modelElement) {

    view.innerHTML += 
    `
    <div class="list-group-item d-flex flex-row justify-content-between" id="task-${modelElement.id}" data-task-id="${modelElement.id}" data-task-text="${modelElement.task}">
        <div>
            <p>${modelElement.task}</p>
        </div>
        <div>
            <button class="btn" type="button" onclick="update(${modelElement.id}, '${modelElement.task}', ${!modelElement.fav})"><i class="bi ${getStarIcon(modelElement.fav)}"></i></button>
        </div>
        <div>
            <button class="btn" type="button" onclick="deleteTask(${modelElement.id})"><i class="bi bi-trash3"></i></button>
        </div>
    </div>
    `
}

// UPDATE MODEL
function submitTask() {
    const taskInput = document.getElementById("task-input");
    const list = document.getElementById('task-list');

    fetch('../api/todos/',
        {
            method: "POST",
            headers: new Headers({"Content-Type": "application/json"}),
            body: JSON.stringify({
                task: taskInput.value
            })
        }
    ).then(response => {
        // UPDATE VIEW
        if (response.status === 201) {
            response.json().then(
                json => {
                    updateViewWithListItem(list, json)
                }
            )
            taskInput.value = "";
        }
    });
}

// UPDATE VIEW
function refreshTaskList() {
    console.log("Fetching task list")
    const list = document.getElementById('task-list');

    fetch('../api/todos').then(
        response => {
            if (response.status === 200) {
                response.json().then(
                    json => {
                        list.innerHTML = ''; // reset list of tasks
                        json.forEach(function (element) {
                            updateViewWithListItem(list, element)
                    });
                });
            }
    });


}

window.onload = function (){refreshTaskList()};
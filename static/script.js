function confirmDelete() {
    return confirm("Are you sure you want to delete this student?");
}

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("studentSearch");
    const studentRows = document.querySelectorAll(".student-row");

    if (!searchInput) {
        return;
    }

    searchInput.addEventListener("input", function () {
        const searchText = searchInput.value.toLowerCase().trim();

        studentRows.forEach(function (row) {
            const rowText = row.textContent.toLowerCase();

            if (rowText.includes(searchText)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }
        });
    });
});
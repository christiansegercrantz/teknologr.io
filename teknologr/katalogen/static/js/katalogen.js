/**
 * Order the rows of a table according to a specific column.
 */
const sortTable = ({ tbody, column, reverse, from_attribute }) => {
    const selector = `td:eq(${column})`;

    // The data to order can be gotten from either the cell text itself or from the 'order-data' attribute, since ordering by the text is not always suitable. For example names might want to be ordered by surname but displayed as "<first_names> <surname>", and dates might be displayed in a certain format but must (and can) be compared using the YYYY-MM-DD format.
    let getData;
    if (from_attribute) {
        getData = a => $(selector, a).attr("order-data") || "";
    } else {
        getData = a =>  $(selector, a).text();
    }

    // localeCompare() can compare numbers as strings when the 'numeric' option is set.
    // XXX: The locale is hardcoded to 'sv' here, but it should probably be handled in some other way
    const compareFn = (a, b) => getData(b).localeCompare(getData(a), "sv", { usage: "sort", sensitivity: "base", numeric: true });

    let rows = tbody.find("tr");
    if (reverse) {
        rows = rows.sort((a, b) => compareFn(a, b));
    } else {
        rows = rows.sort((a, b) => compareFn(b, a));
    }
    rows.appendTo(tbody);
}


$(document).ready(() => {
    /**
     * Setup tables to be sortable by listening for clicks on '.order-by' columns. The order is reversed if the same column is clicked twice in a row. The data location and method of comparison can be changed by adding the classes 'attributes' and 'dates'.
     */
    $(".order-by").each((_, e) => {
        const tbody = $(e).closest("thead").next("tbody");
        if (!tbody) return;

        const column = $(e).closest("th").index().toString();

        e.onclick = () => {
            const by = tbody.attr("order-by");
            let reverse = Boolean(tbody.attr("order-reverse"));
            if (by === column) reverse = !reverse;
            sortTable({
                tbody,
                column,
                reverse,
                from_attribute: $(e).hasClass("attribute"),
            });
            tbody.attr("order-by", column);
            tbody.attr("order-reverse", reverse ? "1" : "");
        }
    });
});

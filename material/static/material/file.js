// Get a reference to the div element where the canvas elements will be added
var pdfContainer = document.getElementById('pdf-container');

    // Get the canvas element where the PDF will be displayed
    // Set the scale (zoom) level of the PDF
    

    // Load the PDF file using the fileUrl variable
    pdfjsLib.getDocument(fileUrl).promise.then(function(pdf) {


    // Get the total number of pages in the PDF
    var numPages = pdf.numPages;

// Loop through each page of the PDF
for (var pageNum = 1; pageNum <= numPages; pageNum++) {
    // Get the current page
    pdf.getPage(pageNum).then(function(page) {

        // Create a new canvas element for this page
        var pageCanvas = document.createElement('canvas');

        // Append the canvas element to the div element
        pdfContainer.appendChild(pageCanvas);

         // Get the context of the canvas
         var pageContext = pageCanvas.getContext('2d');

         // Set the dimensions of the canvas to match the size of the page
         var viewport = page.getViewport({ scale: scale });
         pageCanvas.height = viewport.height;
         pageCanvas.width = viewport.width;

         // Render the page on the canvas
         var renderContext = {
             canvasContext: pageContext,
             viewport: viewport
         };
         page.render(renderContext);

     });
 }
});

function goBack() {
    window.history.back();
}
 
/* Load the PolymerElement base class and html helper function */
import { PolymerElement, html } from '@polymer/polymer/polymer-element.js';
import '@polymer/paper-checkbox/paper-checkbox.js';
/* Load shared styles. All view elements use these styles */
import './shared-styles.js';
/* Load mxGraph */
import '../node_modules/mxgraph/javascript/mxClient.js';

/* Extend the base PolymerElement class */
class MyNewView extends PolymerElement {
  /* Define a template for the new element */
  static get template() {
    return html`
      <style include="shared-styles">
        :host {
          display: block;

          padding: 10px;
        }
      </style>

      <div class="card">
        <div class="circle">1</div>
        <h1>New View</h1>
        <paper-checkbox>Ready to deploy!</paper-checkbox>
        <p>New view!</p>
      </div>
      
      <script type="text/javascript">
      // Program starts here. Creates a sample graph in the
      // DOM node with the specified ID. This function is invoked
      // from the onLoad event handler of the document (see below).
      function main(container)
      {
         // Checks if the browser is supported
         if (!mxClient.isBrowserSupported())
         {
            mxUtils.error('Browser is not supported!', 200, false);
         }
         else
         {
            // Creates the graph inside the given container
            var graph = new mxGraph(container);

            // Enables rubberband selection
            new mxRubberband(graph);

            // Gets the default parent for inserting new cells. This
            // is normally the first child of the root (ie. layer 0).
            var parent = graph.getDefaultParent();

            // Adds cells to the model in a single step
            graph.getModel().beginUpdate();
            try
            {
               var v1 = graph.insertVertex(parent, null,
                        'Hello,', 20, 20, 80, 30);
               var v2 = graph.insertVertex(parent, null,
                        'World!', 200, 150, 80, 30);
               var e1 = graph.insertEdge(parent, null, '', v1, v2);
            }
            finally
            {
               // Updates the display
               graph.getModel().endUpdate();
            }
         }
      };
   </script>
    `;
  }
}
/* Register the new element with the browser */
window.customElements.define('my-new-view', MyNewView);
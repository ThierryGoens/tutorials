/** @odoo-module **/

import { Component, markup } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components ={ Counter, Card }

    value1 = "<div>some text 1</div>";
    value2 = markup("<div>some text 2</div>");

}
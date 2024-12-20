import Controller from "sap/ui/core/mvc/Controller";
import CustomListItem from "sap/m/CustomListItem";
import Input from "sap/m/Input";
import Select from "sap/m/Select";
import MessageBox from "sap/m/MessageBox";
import MessageStrip from "sap/m/MessageStrip";
import List from "sap/m/List";
import HBOX from "sap/m/HBox";
import Text from "sap/m/Text";
import JSONModel from "sap/ui/model/json/JSONModel";
import Icon from "sap/ui/core/Icon";
import { Selectors } from "playwright";


type Query = {
 question: string,
 answer: string
}


export default class MessageList extends Controller {

    async getAnswer(question: string): Promise<string> {
     const response = await fetch(`http://127.0.0.1:8086/${question}`);
     const json = await response.json() as Query;
     (this.getView()?.getModel() as JSONModel).setData(json);
     return json.answer;
    }

    onAskQuestion(): void {
        const selectKey = this.byId("key") as Select;
        const key = selectKey.getSelectedKey();
        console.log("key:" + key);

        const oKeywordInput = this.byId("keywordInput") as Input;
        const keyword = oKeywordInput.getValue();

        const selectPublicationYearFrom = this.byId("selectPublicationYearFrom") as Select;
        const publicationYearFrom = selectPublicationYearFrom.getSelectedKey();
        console.log("publication:" + publicationYearFrom);

        const selectPublicationYearTo = this.byId("selectPublicationYearTo") as Select;
        const publicationYearTo = selectPublicationYearTo.getSelectedKey();
        console.log("publication:" + publicationYearTo);

        const oInput = this.byId("chatInput") as Input;
        const request = oInput.getValue();
        const question = request + "+++" +publicationYearFrom + "+++" + publicationYearTo + "+++" + key + "+++" + keyword;
        console.log(question);
        this.getAnswer(question).then((result: string) => {
            
            console.log(result);
            const oList = this.byId("chatList") as List;

            const questionText = new Text({ text: "You\n" + request + "\n" });
            const questionIcon = new Icon({
                src: "sap-icon://person-placeholder",
                size: "1rem",
            });
            questionIcon.addStyleClass("iconMargin");
            const questionHBox = new HBOX({
                items: [
                    questionIcon,
                    questionText
                ],
                alignItems: "Center"
            });

            const questionItem = new CustomListItem({
                content: questionHBox
            });
            oList.addItem(questionItem);


            const answerText = new Text({ text: "ChatBot\n" + result + "\n" });
            const answerIcon = new Icon({
                src: "sap-icon://ai", 
                size: "1rem", 
            });
            answerIcon.addStyleClass("iconMargin");

            const answerHBox = new HBOX({
                items: [
                    answerIcon,
                    answerText
                ],
                alignItems: "Center"
            });
            answerHBox.addStyleClass("textRightAlign"); 

            const answerItem = new CustomListItem({
                content: answerHBox
            });
            oList.addItem(answerItem);

            selectPublicationYearFrom.setSelectedItem(null);
            selectPublicationYearTo.setSelectedItem(null);




        }).catch(() => {
            MessageBox.alert(`Failure while getting answer...`, {
                actions: MessageBox.Action.CLOSE 
            });
        });;
        oInput.setValue("");
    } 
};
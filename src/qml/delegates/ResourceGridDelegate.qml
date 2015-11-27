import QtQuick 2.5
import QtQuick.Controls 1.4

import "../components"

Item {

    id: root
    property bool selected: false
    property bool isPairA: false
    property bool isPairB: false
    objectName: "resourceDelegate"

    signal itemToggled(int index, bool doClear)
    signal itemDropped(int index)
    signal performMultiSelection(int index)
    
    function refreshInitialPairIndicators() {
        root.isPairA = currentJob.modelData.isPairA(model.url);
        root.isPairB = currentJob.modelData.isPairB(model.url);
    }
    function refreshSelectionState() {
        selected = isSelected(index);
    }

    width: GridView.view.cellWidth
    height: GridView.view.cellHeight
    Component.onCompleted: refreshInitialPairIndicators()

    Menu {
        id: contextMenu
        MenuItem {
            text: root.selected ? "Unselect":"Select"
            onTriggered: itemToggled(index, false)
        }
        MenuItem {
            text: "Open parent directory"
            onTriggered: {
                var urlStr = model.url.toString();
                Qt.openUrlExternally(urlStr.substring(0, urlStr.lastIndexOf('/')));
            }
        }
        MenuSeparator {}
        MenuItem {
            text: "Open job settings"
            onTriggered: settingsOpened()
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        anchors.margins: 2
        drag.target: tile
        cursorShape: Qt.PointingHandCursor
        hoverEnabled: true
        acceptedButtons: Qt.LeftButton | Qt.RightButton
        onClicked: {
            if(mouse.button == Qt.LeftButton){
                if(mouse.modifiers & Qt.ShiftModifier) {
                    performMultiSelection(index);
                    return;
                }
                if(mouse.modifiers & Qt.ControlModifier) {
                    itemToggled(index, false);
                    return;
                }
                if(mouse.button == Qt.LeftButton){
                    itemToggled(index, true);
                    return;
                }
            }
            contextMenu.popup();
        }
        onReleased: {
            if(!tile.Drag.active)
                return;
            tile.Drag.drop();
            itemDropped(index);
        }
        Rectangle {
            id: tile
            property string url: model.url
            color: root.highlighted ? "#A00" : root.selected ? "#5BB1F7" : "#99111111"
            width: mouseArea.width
            height: mouseArea.height
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            Drag.active: mouseArea.drag.active
            Drag.hotSpot.x: tile.width/2
            Drag.hotSpot.y: tile.height/2
            states: State {
                when: mouseArea.drag.active
                ParentChange { target: tile; parent: _mainWindow.contentItem }
                AnchorChanges { target: tile; anchors.verticalCenter: undefined; anchors.horizontalCenter: undefined }
            }
        }
        Image {
            anchors.fill: parent
            anchors.margins: 2
            sourceSize.width: 256
            sourceSize.height: 256
            source: model.url
            fillMode: Image.PreserveAspectCrop
            asynchronous: true
            Rectangle {
                id: container
                width: parent.width
                height: childrenRect.height
                color: "#99000000"
                Behavior on height { NumberAnimation {} }
                Text {
                    width: parent.width
                    text: model.name
                    verticalAlignment: Text.AlignVCenter
                    color: "white"
                    font.pixelSize: 10
                    elide: Text.ElideRight
                    wrapMode: Text.WrapAnywhere
                    maximumLineCount: (mouseArea.containsMouse) ? 4 : 1
                }
            }
            Item {
                id: pairIndicator
                anchors.fill: parent
                visible: root.isPairA || root.isPairB
                Rectangle {
                    anchors.fill: parent
                    color: "black"
                    opacity: 0.5
                }
                CustomText {
                    anchors.centerIn: parent
                    text: root.isPairA ? "A" : "B"
                    textSize: _style.text.size.xlarge
                    color: "#5BB1F7"
                }
            }
            Rectangle { // state indicator (enabled or not)
                anchors.fill: parent
                visible: !root.enabled
                color: "black"
                opacity: 0.5
            }
        }
    }
}
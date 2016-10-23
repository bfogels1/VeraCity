chrome.contextMenus.create({

title: "VeraCity",
contexts:["selection"],
onclick: myFunction

});

function myFunction(selectedText){
	chrome.tabs.create({url: "ec2-35-161-41-36.us-west-2.compute.amazonaws.com:5000/" + selectedText.selectionText})
}

//ec2-35-161-41-36.us-west-2.compute.amazonaws.com
//ec2-35-160-204-88.us-west-2.compute.amazonaws.com
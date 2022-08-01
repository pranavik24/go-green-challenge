// var scoreList = [{name:"amy", score:30}, {name:"betsy", score:100}, {name:"collin", score:50}];
// updateLeaderBoard();
//   scoreList.push({name:"dylan", score:15});
//
//
// var reBtn = document.getElementById("refreshBtn");
// reBtn.addEventListener("click", updateLeaderBoard);
// // let UserScore = class{
// //   constructor(userName, score){
// //     this.userName = userName;
// //     this.score = score;
// //   }
// // }
// function updateLeaderBoard(){
//   var leaderboard = document.getElementById("leaderboard");
//   leaderboard.innerText = "";
// console.log(document.getElementById("leaderboard"));
//
// for(let i = 0; i < scoreList.length; i++){
//   let userName = document.createElement("td");
//   let score = document.createElement("td");
//   score.classList.add("score");
//   userName.classList.add("userName");
//   userName.innerText = scoreList[i].name;
//   score.innerText = scoreList[i].score;
//
//   let scoreLine = document.createElement("tr");
//   scoreLine.classList.add("row");
//   scoreLine.appendChild(userName);
//   scoreLine.appendChild(score);
//   leaderboard.appendChild(scoreLine);
//
// }
// }
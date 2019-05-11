/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
 package tournament;

 import games.MatrixGame;
 import games.MixedStrategy;

 public class AgentUncertainty extends Player{
   protected final String newName = "UnertainStrategy";

   public AgentUncertainty() {
     super();
     playerName = newName;
   }

   protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
     MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
     ms.setZeros();
     int numberOfActions = mg.getNumActions(playerNumber);

     int maxPayChanged = param.getOutcomeUncertainty(); //maximum number of payoffs to be changed
     int maxValueChanged = param.getPayoffUncertainty(); //maximum value by which the payoffs can be changed

     int matrixCount = 0;


     MatrixGame changedGame = mg;
     MixedStrategy tmpMs = new MixedStrategy(mg.getNumActions(playerNumber));
     tmpMs.setZeros();
     int outcome[] = {1,1};
     int cnt = 0;
     boolean newMatrix = false;

     double probs[] = new double[numberOfActions];
     for(int i = 0; i < numberOfActions; i++) probs[i] = 0;

     TotallyMixedStrategy agent = new TotallyMixedStrategy();


     for(int l = 2; l <=4; l++){
       for(int i = 1; i < numberOfActions; i++){
         if(newMatrix){
           newMatrix = false;
           changedGame = mg;
         }
         for(int j = 1; j < numberOfActions; j++){
           cnt++;
           outcome[0] = i;
           outcome[1] = j;
           double payoff = changedGame.getPayoff(outcome, playerNumber);
           changedGame.setPayoff(outcome, playerNumber, payoff+payoff/(maxValueChanged/l));
           if(cnt == maxPayChanged){ //maximum number of payoffs changed, count the probabilities
             newMatrix = true;
             cnt = 0;
             tmpMs = agent.solveGame(changedGame, playerNumber);
             matrixCount++;
             //add probabilities to the strategy
             for(int k = 0; k < numberOfActions; k++){
               probs[k] += tmpMs.getProb(k+1);
             }
           }
         }
       }
     }

     for(int l = 2; l <=4; l++){
       for(int i = 1; i < numberOfActions; i++){
         if(newMatrix){
           newMatrix = false;
           changedGame = mg;
         }
         for(int j = 1; j < numberOfActions; j++){
           cnt++;
           outcome[0] = i;
           outcome[1] = j;
           double payoff = changedGame.getPayoff(outcome, playerNumber);
           changedGame.setPayoff(outcome, playerNumber, payoff-payoff/(maxValueChanged/l));
           if(cnt == maxPayChanged){ //maximum number of payoffs changed, count the probabilities
             newMatrix = true;
             cnt = 0;
             tmpMs = agent.solveGame(changedGame, playerNumber);
             matrixCount++;
             //add probabilities to the strategy
             for(int k = 0; k < numberOfActions; k++){
               probs[k] += tmpMs.getProb(k+1);
             }
           }
         }
       }
     }




     //TODO - change maximum number of values by negative half and set probabilities

     //set probabilites of the strategy
     for(int i = 0; i < numberOfActions; i++){
       ms.setProb(i+1, probs[i]/matrixCount);
     }

     //print probabilities
     System.out.println("probabilities:");
     for(int i = 0; i < numberOfActions; i++){
       System.out.print(ms.getProb(i+1) + " ");
     }
     System.out.println();


     return ms;
   }


 }

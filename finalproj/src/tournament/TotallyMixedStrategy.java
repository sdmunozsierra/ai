// /*
//  * To change this license header, choose License Headers in Project Properties.
//  * To change this template file, choose Tools | Templates
//  * and open the template in the editor.
//  */
package tournament;
import games.MatrixGame;
import games.MixedStrategy;
import tournament.Player;

/**
 *
 * @author Sergio
 * This strategy will use all of our implemented strategies and then Assign
 * a probability factor to each solution by each strategy.
 * -> Run everything and then assign probability factors to each solution.
 */

public class TotallyMixedStrategy extends Player {
    protected final String newName = "TotallyMixedStrategy";

    public TotallyMixedStrategy() {
        super();
        playerName = newName;
    }

    /** Runs a max_min scenario to find the best appropiate action */
    private int max_min(MatrixGame mg, int playerNumber){
      MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
      int act = mg.getNumActions(playerNumber);
      int outcome[] = {0,0};
      double payoffMaxMin = Double.MIN_VALUE;
      int chosenAction = -1;

      //Find Minimum row for player0 and minimum col for player1
      for(int row = 1; row <= act; row++){

        double min = Double.MAX_VALUE; // Set a local maximum
        for(int col = 1; col <= act; col++){
          if (playerNumber == 0){
            outcome[0] = row;
            outcome[1] = col;
          }else{
            outcome[0] = col;
            outcome[1] = row;
          }
          // Get payoff
          double payoff = mg.getPayoff(outcome, playerNumber);
          if(payoff < min)
          min = payoff;
        }

        // Update payoffMaxmin and Chosen Action
        if(chosenAction == -1 || payoffMaxMin < min) {
          payoffMaxMin = min;
          chosenAction = row;
        }

      }//end outer for

      return chosenAction;
    }//end method

    /** Runs a Min_Max scenario to find the best appropiate action */
    private int max_min(MatrixGame mg, int playerNumber){
        MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
        int act = mg.getNumActions(playerNumber);
        int outcome[] = {1,1};
        double payoffMaxMin = Double.MIN_VALUE;
        int chosenPosition = 1;
        double [][] regretTable = new double[act][act];

    //Calculate the probability of choosing that position


      /**
     * GameMaster will call this to compute your strategy.
     * @param mg The game your agent will be playing
     * @param playerNumber Row Player = 1, Column Player = 2
     */
    protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
      MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
      int max_min_result = max_min(mg, playerNumber);
      double[] probability_array = new double[2]; // Currently supports 2 algorithms

      // Check what man min result was
      for(int i = 1; i <= mg.getNumActions(playerNumber); i++){
        // System.out.println("Chosen Action == " + max_min_result + " i == " + i);
        if(i != max_min_result) ms.setProb(i, 0);
        else  ms.setProb(i, 1.0);
      }

      return ms;
    }//End solveGame

  }

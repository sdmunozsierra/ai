// /*
//  * To change this license header, choose License Headers in Project Properties.
//  * To change this template file, choose Tools | Templates
//  * and open the template in the editor.
//  */
package tournament;
import games.MatrixGame;
import games.MixedStrategy;
import tournament.Player;
import tournament.PureNashEquilibrium;

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

  /* Max Min Methods */
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

  /* Min Max Methods */
  /** Runs a Min_Max scenario to find the best appropiate action */
  private int min_max(MatrixGame mg, int playerNumber){
    MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
    int act = mg.getNumActions(playerNumber);
    int outcome[] = {1,1};
    double payoffMaxMin = Double.MIN_VALUE;
    int chosenPosition = 1;
    double [][] regretTable = new double[act][act];

    regretTable = getRegretTable(mg, outcome, playerNumber);

    if(playerNumber == 0){
      //get maximum of each row of the regret table
      double [] max = new double[act];
      for(int row = 0; row < act; row++){
        double rowMax = regretTable[row][0];
        for(int col = 0; col < act; col++){
          if(regretTable[row][col] > rowMax){
            rowMax = regretTable[row][col];
          }
        }
        max[row] = rowMax;
      }
      chosenPosition = get_min_max_position(chosenPosition, max, act);
    }//endif

    else if(playerNumber == 1){ //column player

      //get maximum of each row of the regret table
      double [] max = new double[act];
      for(int col = 0; col < act; col++){
        double rowMax = regretTable[0][col];
        for(int row = 0; row < act; row++){
          if(regretTable[row][col] > rowMax){
            rowMax = regretTable[row][col];
          }
        }
        max[col] = rowMax;
      }
      chosenPosition = get_min_max_position(chosenPosition, max, act);
    }//end else

    return chosenPosition;

  }

  private int get_min_max_position(int chosenPosition, double[] max, int act){
    //find minimum of the maximums
    double min = max[0];
    for(int i = 0; i < act; i++){
      if(max[i] < min){
        min = max[i];
        chosenPosition = i+1;
      }
    }
    return chosenPosition;
  }

  private double[][] getRegretTable(MatrixGame mg, int[] outcome, int playerNumber){
    int act = mg.getNumActions(playerNumber);
    double [][] regretTable = new double[act][act];
    if(playerNumber == 0){

      for(int col = 1; col <= act; col++){
        outcome[0] = 1;
        outcome[1] = col;
        double highest = mg.getPayoff(outcome, playerNumber);
        for(int row = 1; row <= act; row++){ //find highest number of the column
          outcome[0] = row;
          outcome[1] = col;
          if(mg.getPayoff(outcome, playerNumber) > highest){
            highest = mg.getPayoff(outcome, playerNumber);
          }
        }
        //fill in column of the regret table
        for(int r = 0; r < act; r++){
          outcome[0] = r+1;
          regretTable[r][col-1] = highest - mg.getPayoff(outcome, playerNumber);
        }
      }
      return regretTable;

    }else{
      //calculate regret table
      for(int row = 1; row <= act; row++){
        // if(playerNumber == 0){
        //   outcome[0] = 1;
        //   outcome[1] = row;
        // }
        outcome[0] = row;
        outcome[1] = 1;
        double highest = mg.getPayoff(outcome, playerNumber);
        for(int col = 1; col <= act; col++){ //find highest number of the column
          // if(playerNumber == 0){
          //   outcome[0] = col;
          //   outcome[1] = row;
          // }
          outcome[0] = row;
          outcome[1] = col;
          if(mg.getPayoff(outcome, playerNumber) > highest){
            highest = mg.getPayoff(outcome, playerNumber);
          }
        } //fill in column of the regret table
        for(int r = 0; r < act; r++){
          outcome[0] = r+1;
          regretTable[row-1][r] = highest - mg.getPayoff(outcome, playerNumber);
        }
      }
      return regretTable;
    }

  }//end method

  /**
  * GameMaster will call this to compute your strategy.
  * @param mg The game your agent will be playing
  * @param playerNumber Row Player = 1, Column Player = 2
  */
  protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
    MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
    int act = mg.getNumActions(playerNumber);
    int max_min_result = max_min(mg, playerNumber);
    int min_max_result = min_max(mg, playerNumber);
    PureNashEquilibrium ne = new PureNashEquilibrium();
    int pure_nash_result = ne.do_the_nash(mg, playerNumber);

    double[] probability_array = new double[act];
    for (int i=0;i<probability_array.length; i++) {
      probability_array[i] = 0.0;
    }

    // Check what max min result was
    // for(int i = 1; i <= mg.getNumActions(playerNumber); i++){
    //   // System.out.println("Chosen Action == " + max_min_result + " i == " + i);
    //   if(i != max_min_result) ms.setProb(i, 0);
    //   else  ms.setProb(i, 1.0);
    // }

    // System.out.println("MAXMIN Action == " + max_min_result);
    // System.out.println("MINMAX Action == " + min_max_result);
    // System.out.println("PURENASH Action == " + pure_nash_result);

    for(int i = 1; i <= mg.getNumActions(playerNumber); i++){
      if (i == max_min_result)
        probability_array[i-1] += .15;
      if (i == pure_nash_result)
        probability_array[i-1] += .35;
      if (i == min_max_result)
        probability_array[i-1] += .50;

      System.out.println("probability: "+ probability_array[i-1] + " for " + i);
      //Update probability for that choice
      ms.setProb(i, probability_array[i-1]);
    }
    ms.mixWithUniform(0.05);

    System.out.println(ms.toString());

    // Check min max result
    // System.out.println("Chosen Action == " + min_max_result);
    // ms.setZeros();
    // ms.setProb(min_max_result, 1.0);

    // Check pure nash result
    // // System.out.println("Chosen Action == " + pure_nash_result);
    // ms.setZeros();
    // ms.setProb(pure_nash_result, 1.0);
    return ms;
  }//End solveGame

}

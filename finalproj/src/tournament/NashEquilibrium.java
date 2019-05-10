/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tournament;

import games.MatrixGame;
import games.MixedStrategy;
import tournament.Player;

/**
 *
 * @author Sergio & Klara
 */
public class NashEquilibrium extends Player {
    protected final String newName = "NashEquilibrium";

    public NashEquilibrium() {
        super();
        playerName = newName;
    }

    private static double[] findMaxEachRow(double[][] regTable){
      // Find the maximum value for each row
      double[] result = new double[regTable.length];
      for (int i = 0; i < regTable.length; i++) {
        // Assign first element of the row as
        // maximum in first iteration
        double maxNum = regTable[i][0];
        for (int j = 0; j < regTable[i].length; j++) {
          if(maxNum < regTable[i][j]){
            maxNum = regTable[i][j];
          }
          result[i] = maxNum;
        }
      }
      // Display results verbose
      for (int i = 0; i < result.length; i++) {
        System.out.println("Maximum element in row " + (i + 1) + "- " + result[i]);
      }
      return result;
    }

    private static double[] findMaxEachColumn(double[][] regTable){

      // Find the maximum value for each columnn
      double[] result = new double[regTable[0].length];

      // Find longest row
      int longestRow = 0;
      for (int row = 0; row < regTable.length; row++){
        if (regTable[row].length > longestRow){
          longestRow = regTable[row].length;
        }
      }

      // Assign first element of the col as maximum in first iteration
      for ( int col = 0; col < longestRow; col++)
      {
        double highest = Double.MIN_VALUE;
        for ( int row = 0; row < regTable.length; row++)
        if ( col < regTable[row].length && regTable[row][col] > highest){
          highest = regTable[row][col];
          result[col] = highest;
        }
      }
      for (int i = 0; i < result.length; i++) {
        System.out.println("Maximum element in column " + (i + 1) + "- " + result[i]);
      }
      return result;
    }

    // Save MaxValues for all iterations
    double maxCol = Double.MIN_VALUE;
    double maxRow = Double.MIN_VALUE;
    double[] maxColumns;
    double[] maxRows;

    protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
        MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
        int act = mg.getNumActions(playerNumber);
        int outcome[] = {1,1};
        double payoffMaxMin = Double.MIN_VALUE;
        int chosenPosition = 1;
        double [][] regretTable = new double[act][act];
        // int [] chosen_max = new int [2];

        //Nash
        //row player
        if(playerNumber == 0){
          //calculate regret table
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
            } //fill in column of the regret table
            for(int r = 0; r < act; r++){
              outcome[0] = r+1;
              regretTable[r][col-1] = highest - mg.getPayoff(outcome, playerNumber);
            }
          }

          // Find the maximum for each column
          double[] max_cols = findMaxEachColumn(regretTable);

          //find maximum value of all columns
          double max = max_cols[0];
          for(int i = 0; i < act; i++){
            if(max < max_cols[i]){
              max = max_cols[i];
              chosenPosition = i;  // Assign max value of columns to position?
            }
          }
          maxCol = max;  // Save maximum value in global?

        }
        else if(playerNumber == 1){ //column player
            //calculate regret table
            for(int row = 1; row <= act; row++){
              outcome[0] = row;
              outcome[1] = 1;
              double highest = mg.getPayoff(outcome, playerNumber);
              for(int col = 1; col <= act; col++){ //find highest number of the column
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

          // Find the maximum for each Row
          double[] max_rows = findMaxEachRow(regretTable);

          //find maximum of all rows
          double max = max_rows[0];
          for(int i = 0; i < act; i++){
            if(max < max_rows[i]){
              max = max_rows[i];
              chosenPosition = i; // Assign max value of columns to position?
            }
          }
          maxRow = max;  // Save maximum value in global?
        }

        // // Check NashEquilibrium??
        // if(playerNumber == 0){
        //   int max_index = 0;
        //   double max = maxColumns[0];
        //   for(int i = 0; i < maxColumns.length; i++){
        //     if(max < maxColumns[i]){
        //       max = maxColumns[i];
        //       max_index = i;
        //     }
        //   }
        //   if (chosenPosition == max_index){
        //     System.out.println("WOAH!");
        //   }
        // }

        ms.setZeros();
        ms.setProb(chosenPosition, 1.0);
        return ms;
    }


}

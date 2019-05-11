package nfg_ai_project.tournament;
import nfg_ai_project.games.MatrixGame;
import nfg_ai_project.games.MixedStrategy;

public class PureNashEquilibrium extends Player{
    protected final String newName = "PureNashEquilibrium"; 
    
    private class pair{
        double row;
        double column;
        
        pair(){
            row = Double.MAX_VALUE;
            column = Double.MAX_VALUE;
        }
    }

    public PureNashEquilibrium() {
        super();
        playerName = newName;
    }
    
    protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
        MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber)); 
        int act = mg.getNumActions(playerNumber);
        int outcome[] = {1,1};
        
        pair[][] table = new pair[act][act];
        
                //print nash eq table
        for(int i = 0; i < act; i++){
            for(int j = 0; j < act; j++){
                table[i][j] = new pair();
            }
        }
       
        //find nash equilibrium for row player - find best of each column
        for(int col = 1; col <= act; col++){
            outcome[0] = 1;
            outcome[1] = col;
            
            double max = mg.getPayoff(outcome, 0);
            for(int row = 1; row <= act; row++){
                outcome[0] = row;
                if(mg.getPayoff(outcome, 0) > max){
                    max = mg.getPayoff(outcome, 0);
                }   
            }
            for(int row = 1; row <= act; row++){ // find positions with max and set them to true
                outcome[0] = row;
                table[row-1][col-1].row = max - mg.getPayoff(outcome, 0);

            }
        }
        
        //find nash equilibrium for column player
        for(int row = 1; row <= act; row++){
            outcome[0] = row;
            outcome[1] = 1;
            
            double max = mg.getPayoff(outcome, 1);
            for(int col = 1; col <= act; col++){
                outcome[1] = col;
                if(mg.getPayoff(outcome, 1) > max){
                    max = mg.getPayoff(outcome, 1);
                }   
            }
            for(int col = 1; col <= act; col++){ // find positions with max and set them to true
                outcome[1] = col;
                table[row-1][col-1].column = max - mg.getPayoff(outcome, 1);
            }
        }
        
        //find nash equilibrium
        double maxPlayer = 0.0;
        int action = -1;
        double minDev = Double.MAX_VALUE;
        
        for(int i = 0; i < act; i++){
            for(int j = 0; j < act; j++){
                //check if it is a nash equilibrium

                if(minDev > table[i][j].row + table[i][j].column){
                    outcome[0] = i+1;
                    outcome[1] = j+1;
                    if(action == -1 || maxPlayer < mg.getPayoff(outcome, playerNumber)){
                        if(playerNumber == 0) action = i+1;
                        else action = j+1;
                        maxPlayer = mg.getPayoff(outcome, playerNumber);
                    }
                }
                
            }
        }
        //set probability 1 to maxPlayer and 0 to the others
        ms.setZeros();
        ms.setProb(action, 1.0);
        return ms;
        
    }
    
}

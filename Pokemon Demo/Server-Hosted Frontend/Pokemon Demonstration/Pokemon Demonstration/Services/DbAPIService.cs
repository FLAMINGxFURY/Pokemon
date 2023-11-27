using Pokemon_Demonstration.Data;
using System.Text.Json;
using System.Text;

namespace Pokemon_Demonstration.Services {
    public class DbAPIService : FileAPIService {
        protected override string BASE_ADDR => "http://localhost:8000";
    }        
}

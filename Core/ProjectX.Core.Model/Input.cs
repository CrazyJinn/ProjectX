using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ProjectX.Core.Model
{
    public class Input
    {
        public List<Parameter> ParameterList { get; set; }

        public List<int> ResultList { get; set; }
    }

    public class Parameter
    {
        public string ParameterName { get; set; }

        public List<int> ParameterValueList { get; set; }
    }
}

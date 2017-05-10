using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ProjectX.Core.Model;

namespace ProjectX.Core.Modeling
{
    public class Class1
    {
        public Input GetInput()
        {
            return new Input()
            {
                ParameterList = new List<Parameter>()
                {
                    new Parameter()
                    {
                        ParameterName="X",
                        ParameterValueList = new List<int>()
                        {
                            1,
                            2,
                            3,
                        }
                    },
                    new Parameter()
                    {
                        ParameterName="Y",
                        ParameterValueList = new List<int>()
                        {
                            1,
                            2,
                            3,
                        }
                    },
                },

            };
        }
        
    }
}

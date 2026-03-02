import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { Button } from '@/components/ui/Button';

export default function SchemesPage() {
  // Mock data for schemes
  const schemes = [
    {
      id: 1,
      name: "PM Kisan Samman Nidhi",
      description: "Financial support to farmers",
      eligibility: "Small and marginal farmers",
      amount: "₹6,000/year",
      state: "All India",
      category: "Agriculture",
      status: "Active"
    },
    {
      id: 2,
      name: "Pradhan Mantri Awas Yojana",
      description: "Housing for all scheme",
      eligibility: "EWS/LIG/MIG families",
      amount: "Up to ₹2.67 lakh subsidy",
      state: "All India",
      category: "Housing",
      status: "Active"
    },
    {
      id: 3,
      name: "Ayushman Bharat",
      description: "Health insurance scheme",
      eligibility: "Poor and vulnerable families",
      amount: "₹5 lakh coverage",
      state: "All India",
      category: "Healthcare",
      status: "Active"
    }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Government Schemes</h1>
        <Button variant="primary">
          Search Schemes
        </Button>
      </div>

      <div className="grid gap-4">
        {schemes.map((scheme) => (
          <Card key={scheme.id} className="p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {scheme.name}
                </h3>
                <p className="text-gray-600 mb-3">{scheme.description}</p>
              </div>
              <Badge variant="success">{scheme.status}</Badge>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <p className="text-sm text-gray-500">Amount</p>
                <p className="font-medium">{scheme.amount}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Category</p>
                <p className="font-medium">{scheme.category}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">State</p>
                <p className="font-medium">{scheme.state}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Eligibility</p>
                <p className="font-medium text-sm">{scheme.eligibility}</p>
              </div>
            </div>

            <div className="flex gap-3">
              <Button variant="primary" size="sm">
                Check Eligibility
              </Button>
              <Button variant="secondary" size="sm">
                Save Scheme
              </Button>
              <Button variant="secondary" size="sm">
                View Details
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <div className="text-center py-8">
        <p className="text-gray-500 mb-4">Looking for more schemes?</p>
        <Button variant="primary">
          Browse All Schemes
        </Button>
      </div>
    </div>
  );
}
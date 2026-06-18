# Pinsearch Public Search API

Retrieve Indian PIN code information using one or more search parameters. The endpoint supports searching by PIN code, state name, and district name in a single request.

## Base Endpoint

```txt
https://pinsearch.amit4218.fun/api/v1/public
```

## Rate Limits

- 30 requests per minute
- 1000 requests per day

## Query Parameters

| Parameter    | Type   | Required | Description                 |
| ------------ | ------ | -------- | --------------------------- |
| `code`       | string | No       | A 6-digit Indian PIN code.  |
| `state_name` | string | No       | Name of an Indian state.    |
| `district`   | string | No       | Name of an Indian district. |

At least one parameter should be provided.

---

## Search by PIN Code

### Request

```http
GET /api/v1/public?code=734001
```

### Response

```json
{
  "pincode_data": {
    "circlename": "West Bengal Circle",
    "regionname": "North Bengal Region",
    "divisionname": "Darjeeling Division",
    "officename": "Vivekanandapally SO",
    "pincode": "734001",
    "officetype": "PO",
    "delivery": "Non Delivery",
    "district": "JALPAIGURI",
    "statename": "WEST BENGAL",
    "latitude": 26.7166389,
    "longitude": 88.4394722
  }
}
```

---

## Search by State

### Request

```http
GET /api/v1/public?state_name=West Bengal
```

### Response

```json
{
  "state_data": [
        {
        "circlename": "West Bengal Circle",
        "regionname": "North Bengal Region",
        "divisionname": "Darjeeling Division",
        "officename": "Vivekanandapally SO",
        "pincode": "734001",
        "officetype": "PO",
        "delivery": "Non Delivery",
        "district": "JALPAIGURI",
        "statename": "WEST BENGAL",
        "latitude": 26.7166389,
        "longitude": 88.4394722
    },
    {...},
    {...}
  ]
}
```

---

## Search by District

### Request

```http
GET /api/v1/public?district=Darjiling
```

### Response

```json
{
  "district_data": [
    {
        "circlename": "West Bengal Circle",
        "regionname": "North Bengal Region",
        "divisionname": "Darjeeling Division",
        "officename": "Vivekanandapally SO",
        "pincode": "734001",
        "officetype": "PO",
        "delivery": "Non Delivery",
        "district": "JALPAIGURI",
        "statename": "WEST BENGAL",
        "latitude": 26.7166389,
        "longitude": 88.4394722
    },
    {...},
    {...}
  ]
}
```

---

## Combined Search

Multiple filters can be supplied in a single request.

### Request

```http
GET /api/v1/public?code=734001&state_name=West%20Bengal&district=Darjiling
```

### Response

```json
{
  "pincode_data": {
    ...
  },
  "state_data": [...],
  "district_data": [...]
}
```

---

## Response Fields

### `pincode_data`

Returned when the `code` parameter is provided and a matching PIN code is found.

### `state_data`

Returned when the `state_name` parameter is provided and matching records exist.

### `district_data`

Returned when the `district` parameter is provided and matching records exist.

Only fields containing data are included in the response.

---

## Error Handling

### Invalid Request

```json
{
  "detail": "Validation error"
}
```

### No Results Found

```json
{}
```

### Api Rate Limit Hit

```json
{ "error": "Rate limit exceeded: 30 per 1 minute" }
```

An empty object indicates that no matching records were found for the supplied search parameters.

---

## Example cURL

```bash
curl "https://pinsearch.amit4218.fun/api/v1/public?code=734001"
```

## Example JavaScript

```javascript
const response = await fetch(
  "https://pinsearch.amit4218.fun/api/v1/public?code=734001",
);

const data = await response.json();
console.log(data);
```

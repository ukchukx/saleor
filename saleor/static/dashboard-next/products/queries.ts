import gql from "graphql-tag";
import { Query, QueryProps } from "react-apollo";

import {
  ProductCreateDataQuery,
  ProductDetailsQuery,
  ProductDetailsQueryVariables,
  ProductImageQuery,
  ProductImageQueryVariables,
  ProductListQuery,
  ProductListQueryVariables,
  ProductVariantCreateDataQuery,
  ProductVariantCreateDataQueryVariables,
  ProductVariantDetailsQuery,
  ProductVariantDetailsQueryVariables
} from "../gql-types";

export const fragmentMoney = gql`
  fragment Money on Money {
    amount
    currency
  }
`;

export const fragmentProductImage = gql`
  fragment ProductImage on ProductImage {
    id
    alt
    sortOrder
    url
  }
`;

export const fragmentProduct = gql`
  ${fragmentProductImage}
  ${fragmentMoney}
  fragment Product on Product {
    id
    name
    description
    seoTitle
    seoDescription
    category {
      id
      name
    }
    collections {
      edges {
        node {
          id
          name
        }
      }
    }
    price {
      ...Money
    }
    margin {
      start
      stop
    }
    purchaseCost {
      start {
        ...Money
      }
      stop {
        ...Money
      }
    }
    isPublished
    chargeTaxes
    availableOn
    attributes {
      attribute {
        id
        slug
        name
        values {
          name
          slug
        }
      }
      value {
        id
        name
        slug
      }
    }
    availability {
      available
      priceRange {
        start {
          net {
            ...Money
          }
        }
        stop {
          net {
            ...Money
          }
        }
      }
    }
    images {
      edges {
        node {
          ...ProductImage
        }
      }
    }
    variants {
      edges {
        node {
          id
          sku
          name
          priceOverride {
            ...Money
          }
          stockQuantity
          margin
        }
      }
    }
    productType {
      id
      name
      hasVariants
    }
    url
  }
`;

export const fragmentVariant = gql`
  ${fragmentMoney}
  ${fragmentProductImage}
  fragment ProductVariant on ProductVariant {
    id
    attributes {
      attribute {
        id
        name
        slug
        values {
          id
          name
          slug
        }
      }
      value {
        id
        name
        slug
      }
    }
    costPrice {
      ...Money
    }
    images {
      edges {
        node {
          id
        }
      }
    }
    name
    priceOverride {
      ...Money
    }
    product {
      id
      images {
        edges {
          node {
            ...ProductImage
          }
        }
      }
      name
      thumbnailUrl
      variants {
        totalCount
        edges {
          node {
            id
            name
            sku
            image: images(first: 1) {
              edges {
                node {
                  id
                  url
                }
              }
            }
          }
        }
      }
    }
    sku
    quantity
    quantityAllocated
  }
`;

export const TypedProductListQuery = Query as React.ComponentType<
  QueryProps<ProductListQuery, ProductListQueryVariables>
>;

export const productListQuery = gql`
  ${fragmentMoney}
  query ProductList($first: Int, $after: String, $last: Int, $before: String) {
    products(before: $before, after: $after, first: $first, last: $last) {
      edges {
        node {
          id
          name
          thumbnailUrl
          availability {
            available
          }
          price {
            ...Money
          }
          productType {
            id
            name
          }
        }
      }
      pageInfo {
        hasPreviousPage
        hasNextPage
        startCursor
        endCursor
      }
    }
  }
`;

export const TypedProductDetailsQuery = Query as React.ComponentType<
  QueryProps<ProductDetailsQuery, ProductDetailsQueryVariables>
>;

export const productDetailsQuery = gql`
  ${fragmentProduct}
  query ProductDetails($id: ID!) {
    product(id: $id) {
      ...Product
    }
    collections {
      edges {
        node {
          id
          name
        }
      }
    }
    categories {
      edges {
        node {
          id
          name
        }
      }
    }
  }
`;

export const TypedProductVariantQuery = Query as React.ComponentType<
  QueryProps<ProductVariantDetailsQuery, ProductVariantDetailsQueryVariables>
>;

export const productVariantQuery = gql`
  ${fragmentVariant}
  query ProductVariantDetails($id: ID!) {
    productVariant(id: $id) {
      ...ProductVariant
    }
  }
`;

export const TypedProductCreateQuery = Query as React.ComponentType<
  QueryProps<ProductCreateDataQuery>
>;
export const productCreateQuery = gql`
  query ProductCreateData {
    productTypes {
      edges {
        node {
          id
          name
          hasVariants
          productAttributes {
            edges {
              node {
                id
                slug
                name
                values {
                  id
                  sortOrder
                  name
                  slug
                }
              }
            }
          }
        }
      }
    }
    collections {
      edges {
        node {
          id
          name
        }
      }
    }
    categories {
      edges {
        node {
          id
          name
        }
      }
    }
  }
`;

export const TypedProductVariantCreateQuery = Query as React.ComponentType<
  QueryProps<
    ProductVariantCreateDataQuery,
    ProductVariantCreateDataQueryVariables
  >
>;
export const productVariantCreateQuery = gql`
  query ProductVariantCreateData($id: ID!) {
    product(id: $id) {
      id
      images {
        edges {
          node {
            id
            sortOrder
            url
          }
        }
      }
      productType {
        id
        variantAttributes {
          edges {
            node {
              id
              slug
              name
              values {
                id
                sortOrder
                name
                slug
              }
            }
          }
        }
      }
      variants {
        edges {
          node {
            id
            name
            sku
            image: images(first: 1) {
              edges {
                node {
                  id
                  url
                }
              }
            }
          }
        }
      }
    }
  }
`;

export const TypedProductImageQuery = Query as React.ComponentType<
  QueryProps<ProductImageQuery, ProductImageQueryVariables>
>;
export const productImageQuery = gql`
  query ProductImage($productId: ID!, $imageId: ID!) {
    product(id: $productId) {
      id
      mainImage: imageById(id: $imageId) {
        id
        alt
        url
      }
      images {
        edges {
          node {
            id
            url(size: 48)
          }
        }
        pageInfo {
          hasPreviousPage
          hasNextPage
          startCursor
          endCursor
        }
      }
    }
  }
`;
